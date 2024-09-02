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

import threading
import usb.core
import usb.util
from ...utils import Utils

class Drive:

    device_number = 0

    def __init__(self):
        self.device = None
        self.device_number = 0
        self.device_out = None
        self.device_in = None
        self.device_closed = False
        self.read_data = []
        self.read_semaphore = threading.Semaphore(0)
        self.thread = None

    def init(self, vid=0x2886, pid=0x0007):
        device = usb.core.find(idVendor=vid, idProduct=pid)
        if not device:
            Utils().log.warning("No device found")
            return []

        device_number = -1

        config = device.get_active_configuration()

        for interface in config:
            if interface.bInterfaceClass == 0x03:
                device_number = interface.bInterfaceNumber
                break

        if device_number == -1:
            Utils().log.warning("No device found for device_number == -1")
            return []

        try:
            if device.is_kernel_driver_active(device_number):
                device.detach_kernel_driver(device_number)
        except Exception as e:
            Utils().log.warning(e)

        # Configure endpoints
        device_in, device_out = None, None
        for ep in interface:
            if ep.bEndpointAddress & 0x80:
                device_in = ep
            else:
                device_out = ep

        if not device_in:
            Utils().log.warning("No device found for not device_in")
            return []

        hid = Drive()
        hid.device = device
        hid.device_number = device_number
        hid.device_in = device_in
        hid.device_out = device_out

        self.thread = threading.Thread(target=self.task)
        self.thread.daemon = True
        self.thread.start()

        return hid

    def task(self):
        while not self.device_closed:
            self.read_semaphore.acquire()
            if not self.device_closed:
                self.read_data.append(self.device_in.read(self.device_in.wMaxPacketSize, -1))

    def write(self, data):
        self.read_semaphore.release()
        if not self.device_out:
            self.device.ctrl_transfer(0x21, 0x09, 0x200, self.device_number, data)
            return
        self.device_out.write(data)
        return

    def read(self):
        while len(self.read_data) == 0:
            pass
        return self.read_data.pop(0)

    def close(self):
        self.device_closed = True
        self.read_semaphore.release()
        usb.util.dispose_resources(self.device)