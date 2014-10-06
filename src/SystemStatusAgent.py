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
import re


class SystemStatusAgent:
    def __init__(self, device):
        self.device = device

    def getWifiStatus(self):
        """Possible status:
           disabled | connected | enabled | disconnected
        """
        msg = self.device.shell("dumpsys wifi").encode('utf-8')
        pat = re.compile(r'^Wi-Fi is (\w*)')
        try:
            status = pat.findall(msg)[0]
            if status != "":
                return status
            else:
                raise Exception()
        except Exception:
            print "Fail to acquire WiFi status!"
            return False

    def getCellularDataStatus(self):
        """Possible status:
            0 - DATA_DISCONNECTED (Disconnected. IP traffic not available. )
            1 - DATA_CONNECTING(Currently setting up a data connection.)
            2 - DATA_CONNECTED (Connected. IP traffic should be available.)
            3 - DATA_SUSPENDED (Suspended. The connection is up, but IP traffic is temporarily unavailable.
                For example, in a 2G network, data activity may be suspended when a voice call arrives.)
        """
        msg = self.device.shell('dumpsys telephony.registry').encode('utf-8')
        pat = re.compile(r'mDataConnectionState=([0-3])')
        try:
            status = pat.findall(msg)[0]
            if status in ['0', '1', '2', '3']:
                return status
            else:
                raise Exception()
        except Exception:
            print "Fail to acquire Cellular data connection status!"
            return False

    def getScreenRotationStatus(self):
        """Possible status
           1 - Rotation locked
           0 - Auto Rotation
        """
        msg = self.device.shell('dumpsys window').encode('utf-8')
        pat = re.compile(r'mUserRotationMode=([01])')
        try:
            status = pat.findall(msg)[0]
            if status in ['0', '1']:
                return status
            else:
                raise Exception()
        except Exception:
            print "Fail to acquire screen rotation status!"
            return False

    def getOrientation(self):
        """Possible status:
           0 - portrait
           1 - landscape (left side down)
           2 - portrait (upside down)
           3 - landscape (right side down)
        """
        msg = self.device.shell('dumpsys display').encode('utf-8')
        pat = re.compile(r'mCurrentOrientation=([0-3])')
        try:
            status = pat.findall(msg)[0]
            if status in ['0', '1', '2', '3']:
                return status
            else:
                raise Exception()
        except Exception:
            print "Fail to acquire screen orientation!"
            return False

    def getBatteryLevel(self):
        """return the remaining percentage of battery
        """
        msg = self.device.shell('dumpsys battery').encode('utf-8')
        pat = re.compile(r'level: (\d*)')
        try:
            status = pat.findall(msg)[0]
            if 0 <= int(status) <= 100:
                return status
            else:
                raise Exception()
        except Exception:
            print "Fail to acquire the battery level!"
            return False


if __name__ == '__main__':
    device = EMonkeyDevice()
    test = SystemStatusAgent(device)
    print test.getWifiStatus()
    print test.getCellularDataStatus()
    print test.getOrientation()
    print test.getScreenRotationStatus()
    print test.getBatteryLevel()
