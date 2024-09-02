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
from pvrecorder import PvRecorder

class Detection:

    def __init__(self):
        self.pyaudio = pyaudio.PyAudio()
        self.porcupine = None
        self.recorder = None
        self.stream = None

    def create_porcupine(self, keyword=None, language="en"):
        if keyword:
            keyword_paths = []
            sensitivities = []
            language_model = None
            if language == "zh":
                language_model = "/opt/geekros/model/voice/language/porcupine_params_zh.pv"
            for name, path in keyword:
                keyword_paths.append(path)
                sensitivities.append(0.5)
            self.porcupine = pvporcupine.create(
                access_key="zTGV3YMeYwYREJkJ2BcHym1/VUkH/Ei2yB45M64c+KW1LiLGLjsj7Q==",
                library_path=None,
                model_path=language_model,
                keyword_paths=keyword_paths,
                sensitivities=sensitivities
            )

    def start_recorder(self, device_index=-1):
        if self.porcupine:
            self.recorder = PvRecorder(
                frame_length=self.porcupine.frame_length,
                device_index=device_index
            )
            self.recorder.start()

    def start_stream(self, device_index=0):
        if self.porcupine:
            self.stream = self.pyaudio.open(
                input=True,
                start=False,
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                frames_per_buffer=1024,
                input_device_index=device_index
            )
            self.stream.start_stream()

    def stop(self):
        if self.porcupine:
            self.porcupine.delete()
        if self.recorder:
            self.recorder.delete()
        if self.stream:
            self.stream.stop_stream()
