# Copyright 2024 GEEKROS, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyaudio
import respeaker.usb_hid
from respeaker.spi import spi
from ...utils import Utils

class Microphone:

    mono_mode = 1
    listening_mode = 2
    waiting_mode = 3
    speaking_mode = 4
    volume_mode = 5
    display_mode = 6
    auto_mode = 7

    def __init__(self):
        self.pyaudio = pyaudio.PyAudio()
        self.hid = None
        self.index = None
        self.name = ""
        self.on_init()

    def on_init(self):
        for i in range(self.pyaudio.get_device_count()):
            device = self.pyaudio.get_device_info_by_index(i)
            name = device["name"].encode("utf-8")
            if name.lower().find(b'respeaker') >= 0 and device["maxInputChannels"] > 0:
                self.hid = respeaker.usb_hid.get()
                self.index = i
                self.name = name.decode("utf-8")
                Utils().log.debug(self.index, name.decode("utf-8"))
                self.listening()

    def listening(self, direction=None):
        if direction is None:
            self.write(0, [self.auto_mode, 0, 0, 0])
        else:
            self.write(0, [self.listening_mode, 0, direction & 0xFF, (direction >> 8) & 0xFF])

    def waiting(self):
        self.write(0, [self.waiting_mode, 0, 0, 0])

    def speaking(self, strength, direction):
        self.write(0, [self.speaking_mode, strength, direction & 0xFF, (direction >> 8) & 0xFF])

    def set_color(self, rgb=None, r=0, g=0, b=0):
        if rgb:
            self.write(0, [self.mono_mode, rgb & 0xFF, (rgb >> 8) & 0xFF, (rgb >> 16) & 0xFF])
        else:
            self.write(0, [self.mono_mode, b, g, r])

    def set_color_name(self, name=None):
        if name:
            if name == "red":
                self.write(0, [self.mono_mode, 0x400000 & 0xFF, (0x400000 >> 8) & 0xFF, (0x400000 >> 16) & 0xFF])
            if name == "blue":
                self.write(0, [self.mono_mode, 0x0000FF & 0xFF, (0x0000FF >> 8) & 0xFF, (0x0000FF >> 16) & 0xFF])
            if name == "green":
                self.write(0, [self.mono_mode, 0x00FF00 & 0xFF, (0x00FF00 >> 8) & 0xFF, (0x00FF00 >> 16) & 0xFF])
            if name == "yellow":
                self.write(0, [self.mono_mode, 0xFFFF00 & 0xFF, (0xFFFF00 >> 8) & 0xFF, (0xFFFF00 >> 16) & 0xFF])
            if name == "orange":
                self.write(0, [self.mono_mode, 0xFFA500 & 0xFF, (0xFFA500 >> 8) & 0xFF, (0xFFA500 >> 16) & 0xFF])

    def set_volume(self, volume):
        self.write(0, [self.volume_mode, 0, 0, volume])

    def off(self):
        self.write(0, [self.mono_mode, 0 & 0xFF, (0 >> 8) & 0xFF, (0 >> 16) & 0xFF])

    def write(self, address, data):
        if self.hid:
            data = self.to_bytearray(data)
            length = len(data)
            packet = bytearray([address & 0xFF, (address >> 8) & 0xFF, length & 0xFF, (length >> 8) & 0xFF]) + data
            self.hid.write(packet)
            Utils().log.ignore(("%s" % repr(packet)))
            spi.write(address=address, data=data)

    def close(self):
        if self.hid:
            self.off()
            self.hid.close()
            self.hid = None

    @staticmethod
    def to_bytearray(data):
        if type(data) is int:
            array = bytearray([data & 0xFF])
        elif type(data) is bytearray:
            array = data
        elif type(data) is str:
            array = bytearray(data)
        elif type(data) is list:
            array = bytearray(data)
        else:
            raise Utils().log.warning(str('%s is not supported' % type(data)))
        return array

