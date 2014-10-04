#
# Copyright 2014 Mingyuan Xia and others
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
#   Xinye Lin
#

# Imports the monkeyrunner module used by this program
from MonkeyHelper import EMonkeyDevice
from time import sleep
from SystemStatusAgent import SystemStatusAgent
import os

class CellularAgent:

    def __init__(self,device):
        self.device=device

    def turnOnCellularData(self):
        """ Need root access
        """
        try:
            os.system('adb root > /dev/null')
            self.device.shell('svc data enable').encode('utf-8')
            return True
        except:
            print "Failed to turn on the cellular data."

    def turnOffCellularData(self):
        """ Need root access
        """
        try:
            os.system('adb root > /dev/null')
            self.device.shell('svc data disable').encode('utf-8')
            return True
        except:
            print "Failed to turn off the cellular data."
            return False

    def getCellularDataStatus(self):
        sysAgent=SystemStatusAgent(self.device)
        return sysAgent.getCellularDataStatus()

    def changeCellularDataStatus(self):
        if self.getCellularDataStatus()=='2':
            return self.turnOffCellularData()
        elif self.getCellularDataStatus()=='0':
            return self.turnOnCellularData()
        else:
            print "Cellular Data status unchangable for now."
            return False

if __name__=='__main__':
    device=EMonkeyDevice()
    test=CellularAgent(device)
    print test.getCellularDataStatus()
    print test.changeCellularDataStatus()
    sleep(5)
    print test.turnOffCellularData()
    sleep(5)
    print test.turnOnCellularData()
