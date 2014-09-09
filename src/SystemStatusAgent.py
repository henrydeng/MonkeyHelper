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
from MonkeyHelper import MonkeyRunner
import re

class SystemStatusAgent:

    def __init__(self,device):
        self.device=device

    def getWifiStatus(self):
        """Possible status:
           disabled | connected | enabled | disconnected
        """
        msg=self.device.shell("dumpsys wifi").encode('utf-8')
        pat=re.compile(r'^Wi-Fi is (\w*)')
        try:
            status=pat.findall(msg)[0]
            if status!="":
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
            3 - DATA_SUSPENDED (Suspended. The connection is up, but IP traffic is temporarily unavailable. For example, in a 2G network, data activity may be suspended when a voice call arrives.)
        """
        msg=self.device.shell('dumpsys telephony.registry').encode('utf-8')
        pat=re.compile(r'mDataConnectionState=([0-3])')
        try:
            status=pat.findall(msg)[0]
            if status in ['0','1','2','3']:
                return status
            else:
                raise Exception()
        except Exception:
            print "Fail to acquire Cellular data connection status!"
            return False

        #TODO
        #def getScreenRotationStatus(self):




if __name__=='__main__':
    device=MonkeyRunner.waitForConnection()
    test=SystemStatusAgent(device)
    print test.getWifiStatus()
    print test.getCellularDataStatus()

