# -*- coding: utf-8 -*-
#
#       gstreamer.py
#
#       Copyright 2018 Henry Fuheng Wu <wufuheng@gmail.com>
#       Copyright 2012 David Klasinc <bigwhale@lubica.net>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
# PYTHONUNBUFFERED=1;GST_DEBUG=*:3,*ringbuffer*:2;GTK_THEME=Yaru
import logging
import os

logger = logging.getLogger("GStreamer")

import gi
import tempfile
import multiprocessing

#
# This needs to be set before we load GStreamer modules!
#
os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/tmp"
os.putenv("GST_DEBUG_DUMP_DOT_DIR", "/tmp")

gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')

from gi.repository import GObject, Gst, GstVideo

from kazam.frontend.window_webcam import WebcamWindow
from kazam.backend.prefs import *
from kazam.backend.utils import is_xdotool_installed, show_popup

GObject.threads_init()
Gst.init(None)
if prefs.debug:
    Gst.debug_set_active(True)
else:
    Gst.debug_set_active(False)


class Screencast(GObject.GObject):
    __gsignals__ = {"flush-done": (GObject.SIGNAL_RUN_LAST,
                                   None,
                                   (),),
                    }

    def __init__(self, mode):
        GObject.GObject.__init__(self)
        self.temp_fh = tempfile.mkstemp(prefix="kazam_", dir=prefs.video_dest, suffix=".movie")
        self.tempfile = self.temp_fh[1]
        self.muxer_tempfile = "{0}.mux".format(self.tempfile)
        self.pipeline = Gst.Pipeline()
        self.area = None
        self.xid = None
        self.crop_vid = False
        self.mode = mode

    def setup_sources(self,
                      video_source,
                      audio_source,
                      audio2_source,
                      area,
                      xid,
                      audio_channels,
                      audio2_channels):

        # Get the number of cores available then use all except one for encoding
        self.cores = multiprocessing.cpu_count()

        if self.cores > 1:
            self.cores -= 1

        self.audio_source = audio_source
        self.audio_channels = audio_channels
        self.audio2_source = audio2_source
        self.audio2_channels = audio2_channels
        self.video_source = video_source
        self.area = area
        self.xid = xid

        logger.debug("Audio_source : {0}".format(audio_source))
        logger.debug("Audio2_source : {0}".format(audio2_source))
        logger.debug("Video_source: {0}".format(video_source))
        logger.debug("Xid: {0}".format(xid))
        logger.debug("Area: {0}".format(area))

        if self.mode == MODE_BROADCAST:
            logger.debug("Capture Cursor: {0}".format(prefs.capture_cursor_broadcast))
        else:
            logger.debug("Capture Cursor: {0}".format(prefs.capture_cursor))

        logger.debug("Framerate : {0}".format(prefs.framerate))

        if self.video_source or self.area:
            ret = self.setup_video_source()
            if not ret:
                return False

        self.setup_audio_sources()

        if self.mode == MODE_BROADCAST:
            self.setup_rtmpsink()
        else:
            self.setup_filesink()
        self.setup_pipeline()
        self.setup_links()

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self.on_eos)
        self.bus.connect("message::error", self.on_error)
        self.last_err_msg = None

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)
        return True

    def setup_video_source(self):

        if prefs.test:
            self.video_src = Gst.ElementFactory.make("videotestsrc", "video_src")
            self.video_src.set_property("pattern", "smpte")
        elif self.mode in [MODE_SCREENSHOT, MODE_SCREENCAST, MODE_BROADCAST]:
            self.video_src = Gst.ElementFactory.make("ximagesrc", "video_src")
            logger.debug("ximagesrc selected as video source.")
        elif self.mode == MODE_WEBCAM:
            self.video_src = Gst.ElementFactory.make("v4l2src", "video_src")

        if self.area:
            logger.debug("Capturing area.")
            startx = self.area[0] if self.area[0] > 0 else 0
            starty = self.area[1] if self.area[1] > 0 else 0
            endx = self.area[2]
            endy = self.area[3]
        else:
            if self.mode != MODE_WEBCAM:
                startx = self.video_source['x']
                starty = self.video_source['y']
                width = self.video_source['width']
                height = self.video_source['height']
                endx = startx + width - 1
                endy = starty + height - 1
            else:
                startx = 0
                starty = 0
                width = CAM_RESOLUTIONS[prefs.webcam_resolution][0]
                height = CAM_RESOLUTIONS[prefs.webcam_resolution][1]
                endx = CAM_RESOLUTIONS[prefs.webcam_resolution][0] - 1
                endy = CAM_RESOLUTIONS[prefs.webcam_resolution][1] - 1
        if isinstance(self.video_source, dict) and 'scale' in self.video_source:
            scale = self.video_source['scale']
        else:
            scale = 1
        startx = int(startx * scale)
        starty = int(starty * scale)
        endx = int(endx * scale)
        endy = int(endy * scale)
        #
        # H264 requirement is that video dimensions are divisible by 2.
        # If they are not, we have to get rid of that extra pixel.
        #
        if not abs(startx - endx) % 2 and prefs.codec == CODEC_H264:
            endx -= 1

        if not abs(starty - endy) % 2 and prefs.codec == CODEC_H264:
            endy -= 1

        logger.debug("Coordinates SX: {0} SY: {1} EX: {2} EY: {3}".format(startx, starty, endx, endy))

        if prefs.test:
            logger.info("Using test signal instead of screen capture.")
            self.video_caps = Gst.caps_from_string("video/x-raw, framerate={0}/1".format(int(prefs.framerate)))
            self.f_video_caps = Gst.ElementFactory.make("capsfilter", "vid_filter")
            self.f_video_caps.set_property("caps", self.video_caps)
        else:
            if self.mode == MODE_SCREENCAST:
                logger.debug("Testing for xid: {0}".format(self.xid))
                if self.xid:  # xid was passed, so we have to capture a single window.
                    logger.debug("Capturing Window: {0} {1}".format(self.xid, prefs.xid_geometry))
                    window_x, window_y, window_width, window_height = prefs.xid_geometry
                    if is_window_offscreen(window_x, window_y, window_width, window_height):
                        logger.warning("Window is partially or completely off-screen. Moving it on-screen...")
                        nxy = move_window_on_screen(self.xid, window_x, window_y, window_width, window_height)
                        if nxy is None:
                            return False
                        # After moving the window on-screen, create a new tuple with the updated values
                        new_geometry = (nxy[0], nxy[1], prefs.xid_geometry[2], prefs.xid_geometry[3])
                        # Assign the new tuple back to prefs.xid_geometry
                        prefs.xid_geometry = new_geometry
                    self.video_src.set_property("xid", self.xid)

                    if prefs.codec == CODEC_H264:
                        self.video_crop = Gst.ElementFactory.make("videocrop", "cropper")
                        if prefs.xid_geometry[2] % 2:
                            self.video_crop.set_property("left", 1)
                            self.crop_vid = True
                        if prefs.xid_geometry[3] % 2:
                            self.video_crop.set_property("bottom", 1)
                            self.crop_vid = True
                else:
                    self.video_src.set_property("startx", startx)
                    self.video_src.set_property("starty", starty)
                    self.video_src.set_property("endx", endx)
                    self.video_src.set_property("endy", endy)

                self.video_src.set_property("use-damage", False)
                self.video_src.set_property("show-pointer", prefs.capture_cursor)
                self.video_caps = Gst.caps_from_string("video/x-raw, framerate={}/1".format(int(prefs.framerate)))
                self.f_video_caps = Gst.ElementFactory.make("capsfilter", "vid_filter")
                self.f_video_caps.set_property("caps", self.video_caps)
            elif self.mode == MODE_BROADCAST:
                logger.debug("Setting up MODE_BROADCAST for video.")
                if self.xid:  # xid was passed, so we have to capture a single window.
                    logger.debug("Original Capturing Window: {0} {1}".format(self.xid, prefs.xid_geometry))
                    window_x, window_y, window_width, window_height = prefs.xid_geometry
                    odd_window = (window_width % 2) or (window_height % 2)
                    if window_width % 2 != 0:
                        window_width -= 1
                    if window_height % 2 != 0:
                        window_height -= 1
                    if odd_window:
                        import subprocess
                        command_resize = ["xdotool", "windowsize", str(self.xid), str(window_width), str(window_height)]
                        try:
                            result = subprocess.run(command_resize, check=True, timeout=10)  # 10 seconds timeout
                        except subprocess.TimeoutExpired:
                            show_popup("xdotool timed out!")
                    if is_window_offscreen(window_x, window_y, window_width, window_height):
                        logger.warning("Window is partially or completely off-screen. Moving it on-screen...")
                        nxy = move_window_on_screen(self.xid, window_x, window_y, window_width, window_height)
                        if nxy is None:
                            return False
                        prefs.xid_geometry = (nxy[0], nxy[1], window_width, window_height)
                    else:
                        prefs.xid_geometry = (window_x, window_y, window_width, window_height)
                    self.video_src.set_property("xid", self.xid)
                    logger.debug("New Capturing Window: {0} {1}".format(self.xid, prefs.xid_geometry))
                else:
                    self.video_src.set_property("startx", startx)
                    self.video_src.set_property("starty", starty)
                    self.video_src.set_property("endx", endx)
                    self.video_src.set_property("endy", endy)

                self.video_src.set_property("use-damage", False)
                self.video_src.set_property("show-pointer", prefs.capture_cursor_broadcast)
                self.video_caps = Gst.caps_from_string("video/x-raw, framerate={}/1".format(int(prefs.framerate)))
                self.f_video_caps = Gst.ElementFactory.make("capsfilter", "vid_filter")
                self.f_video_caps.set_property("caps", self.video_caps)

                self.video_parse = Gst.ElementFactory.make("h264parse", "video_parse")
                caps_str = "video/x-h264,level=(string)4.1,profile=main"
                self.video_parse_caps = Gst.caps_from_string(caps_str)
                self.f_video_parse_caps = Gst.ElementFactory.make("capsfilter", "vid_parse_caps")
                self.f_video_parse_caps.set_property("caps", self.video_parse_caps)

            '''elif self.mode == MODE_WEBCAM:
                self.video_src.set_property("device", prefs.webcam_sources[prefs.webcam_source][0])
                logger.debug("Webcam source: {}".format(prefs.webcam_sources[prefs.webcam_source][0]))
                desired_framerate = int(prefs.framerate)
                fallback_framerate = 30
                # Check if the desired framerate is supported
                src_pad = self.video_src.get_static_pad("src")
                caps = src_pad.query_caps(None)
                if is_framerate_supported(caps, desired_framerate, width, height):
                    chosen_framerate = desired_framerate
                else:
                    logger.warning(
                        "Desired framerate {} not supported, falling back to {} fps.".format(desired_framerate,
                                                                                             fallback_framerate))
                    chosen_framerate = fallback_framerate
                caps_str = "video/x-raw, framerate={}/1, width={}, height={}".format(chosen_framerate,
                                                                                     width,
                                                                                     height)
                self.video_caps = Gst.caps_from_string(caps_str)
                self.video_src.set_property("num-buffers", 10)  # Adjust this number as needed
                self.f_video_caps = Gst.ElementFactory.make("capsfilter", "vid_filter")
                self.f_video_caps.set_property("caps", self.video_caps)

                if prefs.webcam_show_preview is True:
                    self.video_flip = Gst.ElementFactory.make("videoflip", "video_flip")
                    self.video_flip.set_property("method", "horizontal-flip")
                    self.tee = Gst.ElementFactory.make("tee", "tee")
                    self.screen_queue = Gst.ElementFactory.make("queue", "screen_queue")
                    self.screen_sink = Gst.ElementFactory.make("xvimagesink", "screen_sink")'''

        self.video_convert = Gst.ElementFactory.make("videoconvert", "videoconvert")
        self.video_rate = Gst.ElementFactory.make("videorate", "video_rate")

        if self.mode is not MODE_BROADCAST:
            logger.debug("Codec: {}".format(CODEC_LIST[prefs.codec][2]))

        #
        # Broadcasting forces H264 codec
        #
        if self.mode == MODE_BROADCAST:

            self.video_convert_caps = Gst.caps_from_string("video/x-raw, format=(string)I420")
            self.f_video_convert_caps = Gst.ElementFactory.make("capsfilter", "vid_convert_caps")
            self.f_video_convert_caps.set_property("caps", self.video_convert_caps)

            self.video_bitrate = 5800
            self.video_enc = Gst.ElementFactory.make(CODEC_LIST[CODEC_H264][1], "video_encoder")
            self.video_enc.set_property("bitrate", self.video_bitrate)
            self.video_enc.set_property("key-int-max", 30)
            self.video_enc.set_property("bframes", 0)
            self.video_enc.set_property("byte-stream", False)
            self.video_enc.set_property("aud", True)
            self.video_enc.set_property("tune", "zerolatency")
            #
            # x264enc supports maximum of four cores
            #
            # self.video_enc.set_property("threads", self.cores if self.cores <= 4 else 4)
            self.mux = Gst.ElementFactory.make("flvmux", "muxer")
            self.mux.set_property("streamable", True)

        else:
            if prefs.codec is not CODEC_RAW:
                self.video_enc = Gst.ElementFactory.make(CODEC_LIST[prefs.codec][1], "video_encoder")

            if prefs.codec == CODEC_RAW:
                self.mux = Gst.ElementFactory.make("avimux", "muxer")
            elif prefs.codec == CODEC_VP8:
                self.video_enc.set_property("cpu-used", 2)
                self.video_enc.set_property("end-usage", "vbr")
                self.video_enc.set_property("target-bitrate", 800000000)
                self.video_enc.set_property("static-threshold", 1000)
                self.video_enc.set_property("token-partitions", 2)
                self.video_enc.set_property("max-quantizer", 30)
                self.video_enc.set_property("threads", self.cores)

                # Good framerate, bad memory
                # self.videnc.set_property("cpu-used", 6)
                # self.videnc.set_property("deadline", 1000000)
                # self.videnc.set_property("min-quantizer", 15)
                # self.videnc.set_property("max-quantizer", 15)
                # self.videnc.set_property("threads", self.cores)

                self.mux = Gst.ElementFactory.make("webmmux", "muxer")
            elif prefs.codec == CODEC_H264:
                self.video_enc.set_property("speed-preset", "ultrafast")
                self.video_enc.set_property("pass", 4)
                self.video_enc.set_property("quantizer", 15)
                #
                # x264enc supports maximum of four cores
                #
                self.video_enc.set_property("threads", self.cores if self.cores <= 4 else 4)
                self.mux = Gst.ElementFactory.make("mp4mux", "muxer")
                self.mux.set_property("faststart", 1)
                self.mux.set_property("faststart-file", self.muxer_tempfile)
                self.mux.set_property("streamable", 1)
            elif prefs.codec == CODEC_HUFF:
                self.mux = Gst.ElementFactory.make("avimux", "muxer")
                self.video_enc.set_property("bitrate", 500000)
            elif prefs.codec == CODEC_JPEG:
                self.mux = Gst.ElementFactory.make("avimux", "muxer")

        self.q_video_src = Gst.ElementFactory.make("queue", "queue_video_source")
        self.q_video_in = Gst.ElementFactory.make("queue", "queue_video_in")
        self.q_video_out = Gst.ElementFactory.make("queue", "queue_video_out")
        return True

    def setup_audio_sources(self):
        if self.audio_source or self.audio2_source:
            logger.debug("Setup audio elements.")
            self.aud_out_queue = Gst.ElementFactory.make("queue", "queue_a_out")
            self.audioconv = Gst.ElementFactory.make("audioconvert", "audio_conv")
            if self.mode == MODE_BROADCAST:
                self.audio_bitrate = 128000
                self.audioenc = Gst.ElementFactory.make("avenc_aac", "audio_encoder")
                self.audioenc.set_property("bitrate", self.audio_bitrate)
                #self.audioenc.set_property("compliance", -2)

                self.aacparse = Gst.ElementFactory.make("aacparse", "aacparse")
                self.aacparse_caps = Gst.caps_from_string("audio/mpeg,mpegversion=4,stream-format=raw")
                self.f_aacparse_caps = Gst.ElementFactory.make("capsfilter", "aacparse_filter")
                self.f_aacparse_caps.set_property("caps", self.aacparse_caps)
            else:
                if prefs.codec == CODEC_VP8:
                    self.audioenc = Gst.ElementFactory.make("vorbisenc", "audio_encoder")
                    self.audioenc.set_property("quality", 1)
                else:
                    self.audioenc = Gst.ElementFactory.make("lamemp3enc", "audio_encoder")
                    self.audioenc.set_property("quality", 0)

        if self.audio_source:
            logger.debug("Audio1 Source:\n  {0}".format(self.audio_source))
            self.audiosrc = Gst.ElementFactory.make("pulsesrc", "audio_src")
            self.audiosrc.set_property("device", self.audio_source)
            if self.mode == MODE_BROADCAST and not self.audio2_source:
                audio_caps = " ".join(["audio/x-raw, format=(string)S16LE, endianness=(int)1234,"
                                       "signed=(boolean)true, width=(int)16, depth=(int)16,",
                                       "rate=(int)44100, channels=(int){}".format(self.audio_channels)])
                self.aud_caps = Gst.caps_from_string(audio_caps)
            else:
                self.aud_caps = Gst.caps_from_string("audio/x-raw, channels=(int){}".format(self.audio_channels))
            self.f_aud_caps = Gst.ElementFactory.make("capsfilter", "aud_filter")
            self.f_aud_caps.set_property("caps", self.aud_caps)

            self.aud_in_queue = Gst.ElementFactory.make("queue", "queue_a_in")

        if self.audio2_source:
            logger.debug("Audio2 Source:\n  {0}".format(self.audio2_source))
            self.audio2src = Gst.ElementFactory.make("pulsesrc", "audio2_src")
            self.audio2src.set_property("device", self.audio2_source)
            if self.mode == MODE_BROADCAST and not self.audio_source:
                audio_caps = " ".join(["audio/x-raw, format=(string)S16LE, endianness=(int)1234,"
                                       "signed=(boolean)true, width=(int)16, depth=(int)16,",
                                       "rate=(int)44100, channels=(int){}".format(self.audio2_channels)])
                self.aud2_caps = Gst.caps_from_string(audio_caps)
            else:
                self.aud2_caps = Gst.caps_from_string("audio/x-raw, channels=(int){}".format(self.audio2_channels))
            self.f_aud2_caps = Gst.ElementFactory.make("capsfilter", "aud2_filter")
            self.f_aud2_caps.set_property("caps", self.aud2_caps)
            self.aud2_in_queue = Gst.ElementFactory.make("queue", "queue_a2_in")
            self.audio2conv = Gst.ElementFactory.make("audioconvert", "audio2_conv")

            self.audio2stereo = Gst.ElementFactory.make("audioconvert", "audio2_stereo")
            self.audio2stereo_caps = Gst.caps_from_string("audio/x-raw, channels=2")
            self.f_audio2stereo_caps = Gst.ElementFactory.make("capsfilter", "audio2stereo_filter")
            self.f_audio2stereo_caps.set_property("caps", self.audio2stereo_caps)

        if self.audio_source and self.audio2_source:
            self.audiomixer = Gst.ElementFactory.make("adder", "audiomixer")
            # if self.mode == MODE_BROADCAST:
            #     mixer_caps = " ".join(["audio/x-raw, format=(string)S16LE, endianness=(int)1234,"
            #                            "signed=(boolean)true, width=(int)16, depth=(int)16,",
            #                            "rate=(int)44100, channels=(int)2"])
            #     self.mixer_caps = Gst.caps_from_string(mixer_caps)
            #     self.f_mixer_caps = Gst.ElementFactory.make("capsfilter", "mixer_filter")
            #     self.f_mixer_caps.set_property("caps", self.mixer_caps)

    def setup_filesink(self):
        self.final_queue = Gst.ElementFactory.make("queue", "queue_final")
        logger.debug("Filesink: {}".format(self.tempfile))
        self.sink = Gst.ElementFactory.make("filesink", "sink")
        self.sink.set_property("location", self.tempfile)

    def setup_rtmpsink(self):
        if self.audio_source or self.audio2_source:
            bitrate = self.video_bitrate + (self.audio_bitrate / 1000)
        else:
            bitrate = self.video_bitrate

        if prefs.broadcast_dst == 0:
            #
            # Broadcast to YouTube
            #
            self.rtmp_location = "".join([prefs.yt_server,
                                          "/x/",
                                          prefs.yt_stream,
                                          "?videoKeyframeFrequency=1&totalDatarate=",
                                          str(bitrate)])
        elif prefs.broadcast_dst == 1:
            #
            # Broadcast to Twitch
            #
            if prefs.tw_server is None:
                print("Please set up Twitch server first")
                return
            if (prefs.tw_server.endswith('/')):
                self.rtmp_location = "".join([prefs.tw_server, prefs.tw_stream])
            else:
                self.rtmp_location = "".join([prefs.tw_server, '/', prefs.tw_stream])

        self.final_queue = Gst.ElementFactory.make("queue", "queue_rtmp")
        logger.debug("RTMP sink: {}".format(self.rtmp_location))
        self.sink = Gst.ElementFactory.make("rtmpsink", "sink")
        self.sink.set_property("location", self.rtmp_location)

    #
    # One day, this horrific code will be optimised... I promise!
    #
    def setup_pipeline(self):
        #
        # Behold, setup the master pipeline
        #
        self.pipeline.add(self.video_src)
        self.pipeline.add(self.f_video_caps)
        self.pipeline.add(self.q_video_src)
        if self.crop_vid and self.mode is not MODE_BROADCAST:
            self.pipeline.add(self.video_crop)
        self.pipeline.add(self.video_rate)
        self.pipeline.add(self.video_convert)
        self.pipeline.add(self.q_video_out)
        self.pipeline.add(self.final_queue)

        if prefs.webcam_show_preview and self.mode == MODE_WEBCAM:
            self.pipeline.add(self.tee)
            self.pipeline.add(self.video_flip)
            self.pipeline.add(self.screen_queue)
            self.pipeline.add(self.screen_sink)

        if prefs.codec is not CODEC_RAW or self.mode == MODE_BROADCAST:
            self.pipeline.add(self.video_enc)

        if self.mode == MODE_BROADCAST:
            self.pipeline.add(self.f_video_convert_caps)
            self.pipeline.add(self.video_parse)
            self.pipeline.add(self.f_video_parse_caps)

        if self.audio_source or self.audio2_source:
            self.pipeline.add(self.audioconv)
            self.pipeline.add(self.audioenc)
            self.pipeline.add(self.aud_out_queue)

            if self.mode == MODE_BROADCAST:
                self.pipeline.add(self.aacparse)
                self.pipeline.add(self.f_aacparse_caps)

        if self.audio_source:
            self.pipeline.add(self.audiosrc)
            self.pipeline.add(self.aud_in_queue)
            self.pipeline.add(self.f_aud_caps)

        if self.audio2_source:
            self.pipeline.add(self.audio2src)
            self.pipeline.add(self.aud2_in_queue)
            self.pipeline.add(self.f_aud2_caps)
            self.pipeline.add(self.audio2stereo)
            self.pipeline.add(self.f_audio2stereo_caps)

        if self.audio_source and self.audio2_source:
            self.pipeline.add(self.audiomixer)
            # if self.mode == MODE_BROADCAST:
            #     self.pipeline.add(self.f_mixer_caps)

        self.pipeline.add(self.mux)
        self.pipeline.add(self.sink)

    # gst-launch-1.0 -e ximagesrc endx=1919 endy=1079 use-damage=false show-pointer=true ! \
    #   queue ! videorate ! video/x-raw,framerate=15/1 ! videoconvert ! \
    #   vp8enc end-usage=vbr target-bitrate=800000000 threads=3 static-threshold=1000 \
    #     token-partitions=2 max-quantizer=30 ! queue name=before_mux ! webmmux name=mux ! \
    #   queue ! filesink location="test-videorate.webm"

    def setup_links(self):
        # Connect everything together
        if self.mode == MODE_BROADCAST:
            ret = self.video_src.link(self.q_video_src)
            logger.debug("Link video_src -> q_video_src: {}".format(ret))
        else:
            ret = self.video_src.link(self.f_video_caps)
            logger.debug("Link video_src -> f_video_caps: {}".format(ret))
            ret = self.f_video_caps.link(self.q_video_src)
            logger.debug("Link f_video_caps -> q_video_src: {}".format(ret))

        if self.mode == MODE_WEBCAM and prefs.webcam_show_preview:
            # Setup camera preview window
            self.cam_window = WebcamWindow(CAM_RESOLUTIONS[prefs.webcam_resolution][0],
                                           CAM_RESOLUTIONS[prefs.webcam_resolution][1],
                                           prefs.webcam_preview_pos,
                                           prefs.webcam_preview_x_offset,
                                           prefs.webcam_preview_y_offset)

            self.cam_xid = self.cam_window.xid

            # Build the pipeline
            self.q_video_src.link(self.tee)
            self.tee.link(self.video_rate)
            self.tee.link(self.video_flip)
            self.video_flip.link(self.screen_queue)
            self.screen_queue.link(self.screen_sink)

        else:
            if self.crop_vid and self.mode is not MODE_BROADCAST:
                ret = self.q_video_src.link(self.video_crop)
                logger.debug("Link q_video_src -> video_crop {}".format(ret))
                ret = self.video_crop.link(self.video_rate)
                logger.debug("Link video_crop -> video_rate {}".format(ret))

            if self.mode == MODE_BROADCAST:
                ret = self.q_video_src.link(self.video_convert)
                logger.debug("Link q_video_src -> video_convert {}".format(ret))
            else:
                ret = self.q_video_src.link(self.video_rate)
                logger.debug("Link q_video_src -> video_rate {}".format(ret))
                ret = self.video_rate.link(self.video_convert)
                logger.debug("Link video_rate -> video_convert: {}".format(ret))

        if prefs.codec is CODEC_RAW and self.mode is not MODE_BROADCAST:
            self.video_convert.link(self.q_video_out)
            logger.debug("Linking RAW Video")
        else:
            logger.debug("Linking Video")
            if self.mode == MODE_BROADCAST:
                ret = self.video_convert.link(self.f_video_convert_caps)
                logger.debug("Link video_convert f_video_convert_caps {}".format(ret))
                ret = self.f_video_convert_caps.link(self.video_enc)
                logger.debug("Link f_video_convert_caps -> video_enc {}".format(ret))
                ret = self.video_enc.link(self.video_parse)
                logger.debug("Link video_enc -> video_parse {}".format(ret))
                ret = self.video_parse.link(self.f_video_parse_caps)
                logger.debug("Link video_parse -> f_video_parse_caps {}".format(ret))
                ret = self.f_video_parse_caps.link(self.q_video_out)
                logger.debug("Link f_video_parse_caps -> q_video_out {}".format(ret))
            else:
                ret = self.video_convert.link(self.video_enc)
                logger.debug("Link video_convert -> video_enc {}".format(ret))
                ret = self.video_enc.link(self.q_video_out)
                logger.debug("Link video_enc -> q_video_out {}".format(ret))

        ret = self.q_video_out.link(self.mux)
        logger.debug("Link q_video_out -> mux {}".format(ret))

        if self.audio_source and self.audio2_source:
            logger.debug("Linking Audio")
            ret = self.audiosrc.link(self.aud_in_queue)
            logger.debug(" Link audiosrc -> aud_in_queue: %s" % ret)
            ret = self.aud_in_queue.link(self.f_aud_caps)
            logger.debug(" Link aud_in_queue -> aud_caps_filter: %s" % ret)

            logger.debug("Linking Audio2")
            # Link first audio source to mixer
            ret = self.f_aud_caps.link(self.audiomixer)
            logger.debug(" Link aud_caps_filter -> audiomixer: %s" % ret)

            # Link second audio source to mixer
            ret = self.audio2src.link(self.aud2_in_queue)
            logger.debug(" Link audio2src -> aud2_in_queue: %s" % ret)
            ret = self.aud2_in_queue.link(self.f_aud2_caps)
            logger.debug(" Link aud2_in_queue -> aud2_caps_filter: %s" % ret)
            # ret = self.f_aud2_caps.link(self.audiomixer)
            # logger.debug(" Link aud2_caps_filter -> audiomixer: %s" % ret)
            ret = self.f_aud2_caps.link(self.audio2stereo)
            logger.debug(" Link aud2_caps_filter -> audio2stereo: %s" % ret)
            ret = self.audio2stereo.link(self.f_audio2stereo_caps)
            logger.debug(" Link audio2stereo -> audio2stereo_caps_filter: %s" % ret)
            ret = self.f_audio2stereo_caps.link(self.audiomixer)
            logger.debug(" Link f_audio2stereo_caps -> audiomixer: %s" % ret)

            # Link mixer to audio convert
            ret = self.audiomixer.link(self.audioconv)
            logger.debug(" Link audiomixer -> audioconv: %s" % ret)

        elif self.audio_source:

            logger.debug("Linking Audio")
            ret = self.audiosrc.link(self.aud_in_queue)
            logger.debug(" Link audiosrc -> aud_in_queue: %s" % ret)
            ret = self.aud_in_queue.link(self.f_aud_caps)
            logger.debug(" Link aud_in_queue -> aud_caps_filter: %s" % ret)

            # Link first audio source to audio convert
            ret = self.f_aud_caps.link(self.audioconv)
            logger.debug(" Link aud_caps_filter -> audioconv: %s" % ret)

        elif self.audio2_source:
            # Link second audio source to mixer
            ret = self.audio2src.link(self.aud2_in_queue)
            logger.debug(" Link audio2src -> aud2_in_queue: %s" % ret)
            ret = self.aud2_in_queue.link(self.f_aud2_caps)
            logger.debug(" Link aud2_in_queue -> aud2_caps_filter: %s" % ret)

            # Link second audio source to audio convert
            ret = self.f_aud2_caps.link(self.audioconv)
            logger.debug(" Link aud2_caps_filter -> audioconv: %s" % ret)

        if self.audio_source or self.audio2_source:
            # Link audio to muxer
            ret = self.audioconv.link(self.audioenc)
            logger.debug("Link audioconv -> audioenc: %s" % ret)
            ret = self.audioenc.link(self.aud_out_queue)
            logger.debug("Link audioenc -> aud_out_queue: %s" % ret)

            if self.mode == MODE_BROADCAST:
                ret = self.aud_out_queue.link(self.aacparse)
                logger.debug("Link aud_out_queue -> aacparse: {}".format(ret))
                ret = self.aacparse.link(self.f_aacparse_caps)
                logger.debug("Link aacparse -> f_aacparse_caps: {}".format(ret))
                ret = self.f_aacparse_caps.link(self.mux)
                logger.debug("Link aacparse_caps_filter -> mux: {}".format(ret))
            else:
                ret = self.aud_out_queue.link(self.mux)
                logger.debug("Link aud_out_queue -> mux: %s" % ret)

        ret = self.mux.link(self.final_queue)
        logger.debug("Link mux -> file queue: %s" % ret)
        ret = self.final_queue.link(self.sink)
        if self.mode == MODE_BROADCAST:
            logger.debug("Link final queue -> rtmp sink: {}".format(ret))
        else:
            logger.debug("Link final queue -> file sink: {}".format(ret))

    def start_recording(self):
        logger.debug("Setting STATE_PLAYING")
        self.pipeline.set_state(Gst.State.PLAYING)

    def pause_recording(self):
        logger.debug("Setting STATE_PAUSED")
        self.pipeline.set_state(Gst.State.PAUSED)

    def unpause_recording(self):
        logger.debug("Setting STATE_PLAYING - UNPAUSE")
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop_recording(self):
        if self.mode == MODE_BROADCAST:
            self.pipeline.set_state(Gst.State.NULL)
            logger.debug("Emitting flush-done.")
            self.emit("flush-done")
        elif self.mode == MODE_WEBCAM:
            logger.debug("Sending new EOS event")
            self.pipeline.send_event(Gst.Event.new_eos())
            print("stop_recording for webcam is done")
        else:
            logger.debug("Sending new EOS event")
            self.pipeline.send_event(Gst.Event.new_eos())

    def get_tempfile(self):
        return self.tempfile

    def get_audio_recorded(self):
        return self.audio

    def on_eos(self, bus, message):
        logger.debug("Received EOS, setting pipeline to NULL.")
        if self.mode == MODE_WEBCAM and prefs.webcam_show_preview:
            self.cam_window.window.destroy()
            self.cam_window = None

        self.pipeline.set_state(Gst.State.NULL)
        logger.debug("Emitting flush-done.")
        self.emit("flush-done")

    def on_error(self, bus, message):
        if message.type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            if self.last_err_msg != err.message:
                error_message = f"Error: {err.message}"
                if debug:
                    error_message += f"\nDebug info: {debug}"
                show_popup(error_message, title="Kazam encountered errors")
                self.last_err_msg = err.message
        logger.debug("Received an error message: %s", message.parse_error()[1])

    def on_sync_message(self, bus, message):
        if message.get_structure().get_name() == 'prepare-window-handle':
            logger.debug("Preparing Window Handle")
            message.src.set_window_handle(self.cam_window.xid)


class GWebcam(GObject.GObject):

    def __init__(self):
        GObject.GObject.__init__(self)
        self.pipeline = Gst.Pipeline()
        self.xid = None

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self.on_eos)
        self.bus.connect("message::error", self.on_error)

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)
        self.pipeline.set_state(Gst.State.PAUSED)

    def start(self):
        width = CAM_RESOLUTIONS[prefs.webcam_resolution][0]
        height = CAM_RESOLUTIONS[prefs.webcam_resolution][1]

        self.video_src = Gst.ElementFactory.make("v4l2src", "video_src")
        self.q_video_src = Gst.ElementFactory.make("queue", "queue_video_source")

        self.video_src.set_property("device", prefs.webcam_sources[prefs.webcam_source][0])
        logger.debug("Webcam source: {}".format(prefs.webcam_sources[prefs.webcam_source][0]))

        desired_framerate = int(prefs.framerate)
        fallback_framerate = 30
        # Check if the desired framerate is supported
        src_pad = self.video_src.get_static_pad("src")
        caps = src_pad.query_caps(None)
        if is_framerate_supported(caps, desired_framerate, width, height):
            chosen_framerate = desired_framerate
        else:
            logger.warning("Desired framerate {} not supported, falling back to {} fps.".format(desired_framerate,
                                                                                                fallback_framerate))
            chosen_framerate = fallback_framerate

        # Clean up the pad after querying capabilities
        # src_pad.unref()
        caps_str = "video/x-raw, framerate={}/1, width={}, height={}".format(chosen_framerate, width, height)
        logger.debug("webcam caps: {}".format(caps_str))
        self.video_caps = Gst.caps_from_string(caps_str)
        self.f_video_caps = Gst.ElementFactory.make("capsfilter", "vid_filter")
        self.f_video_caps.set_property("caps", self.video_caps)
        self.screen_queue = Gst.ElementFactory.make("queue", "screen_queue")
        self.screen_sink = Gst.ElementFactory.make("xvimagesink", "screen_sink")

        self.pipeline.add(self.video_src)
        self.pipeline.add(self.f_video_caps)
        self.pipeline.add(self.q_video_src)
        self.pipeline.add(self.screen_queue)
        self.pipeline.add(self.screen_sink)

        self.cam_window = WebcamWindow(CAM_RESOLUTIONS[prefs.webcam_resolution][0],
                                       CAM_RESOLUTIONS[prefs.webcam_resolution][1],
                                       prefs.webcam_preview_pos,
                                       prefs.webcam_preview_x_offset,
                                       prefs.webcam_preview_y_offset)

        self.cam_xid = self.cam_window.xid
        ret = self.video_src.link(self.f_video_caps)
        logger.debug("Link video_src -> f_video_caps: {}".format(ret))
        ret = self.f_video_caps.link(self.q_video_src)
        logger.debug("Link f_video_caps -> q_video_src: {}".format(ret))
        ret = self.q_video_src.link(self.screen_queue)
        logger.debug("Link q_video_src -> screen_queue: {}".format(ret))
        ret = self.screen_queue.link(self.screen_sink)
        logger.debug("Link screen_queue -> screen_sink: {}".format(ret))
        self.pipeline.set_state(Gst.State.PLAYING)

    def close(self):
        self.pipeline.send_event(Gst.Event.new_eos())
        self.close_pipeline()
        logger.debug("close_pipeline")
        # Destroy the webcam window if it exists
        if self.cam_window is not None:
            logger.debug("Destroying webcam window.")
            self.cam_window.window.destroy()  # Destroy the window
            self.cam_window = None  # Set to None to avoid further operations on it

    def on_eos(self, bus, message):
        logger.debug("Received EOS, setting pipeline to NULL.")
        if self.cam_window:
            self.cam_window.window.destroy()
            self.cam_window = None
        self.pipeline.set_state(Gst.State.NULL)

    def on_error(self, bus, message):
        logger.debug("Received an error message: %s", message.parse_error()[1])

    def on_sync_message(self, bus, message):
        structure = message.get_structure()
        if structure and structure.get_name() == 'prepare-window-handle':
            logger.debug("Preparing Window Handle")
            if isinstance(message.src, GstVideo.VideoOverlay):
                message.src.set_window_handle(self.cam_xid)
            else:
                logger.warning("Current video sink does not support setting a window handle.")

    def close_pipeline(self):
        if self.pipeline is not None:
            self.pipeline.set_state(Gst.State.NULL)
            elements = [self.video_src, self.q_video_src, self.f_video_caps, self.screen_queue, self.screen_sink]
            for element in elements:
                if element is not None:
                    self.pipeline.remove(element)
            self.pipeline = None
            logger.debug("Pipeline and elements successfully removed.")


def is_framerate_supported(caps, framerate, width, height):
    for i in range(caps.get_size()):
        structure = caps.get_structure(i)

        try:
            cap_framerate = structure.get_value('framerate')
        except TypeError:
            logger.warning("Encountered an unknown type while retrieving framerate. Skipping.")
            continue

        if cap_framerate is None:
            continue

        cap_width = structure.get_value('width')
        cap_height = structure.get_value('height')

        # Handle GstFractionRange
        if hasattr(cap_framerate, 'get_min') and hasattr(cap_framerate, 'get_max'):
            min_framerate = cap_framerate.get_min()
            max_framerate = cap_framerate.get_max()
            if (min_framerate.num <= framerate <= max_framerate.num and
                    cap_width == width and cap_height == height):
                return True

        # Handle GstFraction
        elif isinstance(cap_framerate, Gst.Fraction):
            if (cap_framerate.num == framerate and cap_framerate.denom == 1 and
                    cap_width == width and cap_height == height):
                return True

        # Unknown type handling
        else:
            logger.warning(f"Unknown framerate type encountered: {type(cap_framerate)}. Skipping.")
            continue

    return False


def is_window_offscreen(window_x, window_y, window_width, window_height):
    screen_width, screen_height = get_screen_resolution()

    # Check if the window is completely or partially off the left or right side of the screen
    if window_x < 0 or window_x + window_width > screen_width:
        return True  # Offscreen to the left or right

    # Check if the window is completely or partially off the top or bottom of the screen
    if window_y < 0 or window_y + window_height > screen_height:
        return True  # Offscreen to the top or bottom

    return False


def get_screen_resolution():
    from kazam.backend.prefs import HW
    screen = HW.get_current_screen()
    monitor = HW.default_screen.get_monitor_geometry(screen)
    return monitor.width, monitor.height

def move_window_on_screen(xid, window_x, window_y, window_width, window_height):
    if not is_xdotool_installed():
        show_popup("xdotool is not installed. Please move the window completely on-screen manually or install xdotool.")
        return None  # Return None if xdotool is not installed

    screen_width, screen_height = get_screen_resolution()
    import subprocess
    new_x = max(0, min(window_x, screen_width - window_width))
    new_y = max(0, min(window_y, screen_height - window_height))
    command = ["xdotool", "windowmove", str(xid), str(new_x), str(new_y)]
    subprocess.run(command)
    return new_x, new_y

