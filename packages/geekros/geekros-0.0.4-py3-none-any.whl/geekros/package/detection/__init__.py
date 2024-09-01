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
import pvporcupine

class Detection:

    def __init__(self):
        self.pyaudio = pyaudio.PyAudio()
        self.porcupine = None
        self.stream = None

    def create_porcupine(self, keyword="haozhu"):
        self.porcupine = pvporcupine.create(
            access_key="zTGV3YMeYwYREJkJ2BcHym1/VUkH/Ei2yB45M64c+KW1LiLGLjsj7Q==",
            library_path=None,
            model_path=None,
            keyword_paths=["/opt/geekros/model/voice/keyword/" + keyword + ".ppn"],
            sensitivities=[0.5]
        )

    def start_stream(self, device_index=0):
        if self.porcupine:
            self.stream = self.pyaudio.open(
                input=True,
                start=False,
                format=pyaudio.paInt16,
                channels=1,
                rate=self.porcupine.sample_rate,
                frames_per_buffer=self.porcupine.frame_length,
                input_device_index=device_index
            )
            self.stream.start_stream()
