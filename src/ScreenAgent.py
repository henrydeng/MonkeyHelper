#
# Copyright 2014 Mingyuan Xia and others
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Contributors:
#   Xinye Lin
#

# Imports the monkeyrunner module used by this program
from MonkeyHelper import EMonkeyDevice
from SystemStatusAgent import SystemStatusAgent


class ScreenAgent:
    def __init__(self, device):
        self.device = device

    def getScreenRotationStatus(self):
        sysAgent = SystemStatusAgent(self.device)
        return sysAgent.getScreenRotationStatus()

    def getOrientation(self):
        sysAgent = SystemStatusAgent(self.device)
        return sysAgent.getOrientation()


if __name__ == '__main__':
    device = EMonkeyDevice()
    test = ScreenAgent(device)
    print test.getScreenRotationStatus()
    print test.getOrientation()
