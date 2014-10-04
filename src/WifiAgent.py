#
# Copyright 2014 Xinye Lin and others
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
#
# Contributors:
#   Ran Shu
#

# Imports the monkeyrunner module used by this program
from MonkeyHelper import EMonkeyDevice
from time import sleep
from SystemStatusAgent import SystemStatusAgent
import os

class WifiAgent:


    def __init__(self,device):
        self.device=device

    def turnOnWifi(self):
        """ Need root access
        """
        try:
            os.system('adb root > /dev/null')
            self.device.shell('svc wifi enable').encode('utf-8')
            return True
        except:
            print "Failed to turn on the Wifi."
            return False

    def turnOffWifi(self):
        """ Need root access
        """
        try:
            os.system('adb root > /dev/null')
            self.device.shell('svc wifi disable').encode('utf-8')
            return True
        except:
            print "Failed to turn off the Wifi."
            return False

    def getWiFiStatus(self):
        sysAgent=SystemStatusAgent(self.device)
        return sysAgent.getWifiStatus()

    def changeWifiStatus(self):
        status=self.getWiFiStatus()
        if status=='enabled':
            return self.turnOffWifi()
        elif status=='disabled':
            return self.turnOnWifi()
        else:
            print "Wifi status unchangable for now."
            return False

if __name__=='__main__':
    device=EMonkeyDevice()
    test=WifiAgent(device)
    print test.getWiFiStatus()
    print test.changeWifiStatus()
    sleep(5)
    print test.turnOffWifi()
    sleep(5)
    print test.turnOnWifi()
