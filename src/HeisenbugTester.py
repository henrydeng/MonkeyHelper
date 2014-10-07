#
# Copyright 2014 Mingyuan Xia (http://mxia.me) and others
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
import random
from Agents import CellularAgent, LogcatAgent, WifiAgent


class HeisenbugTester:
    def __init__(self, device, package, seed=11, number=10):
        self.device = device
        self.seed = seed
        self.number = number
        self.package = package
        self.logcat = LogcatAgent(self.device)
        #TODO add orientation and other events
        self.specialEvents = ['wifi', 'data']
        random.seed(self.seed)

    def generateSpecialEventSequence(self):
        length = len(self.specialEvents)
        seq = self.specialEvents * (self.number/length+1)
        seq = random.sample(seq, self.number)
        return seq

    def processSpecialEvents(self, specialEvent):
        if specialEvent == 'wifi':
            WifiAgent(self.device).changeWifiStatus()
        elif specialEvent == 'data':
            CellularAgent(self.device).toggleCellularDataStatus()


    def runnerMixEvents(self):
        """run self.number pieces of random special events
           and self.number pieces of random simple events in between of any two continuous special events
        """
        try:
            specialSeq = self.generateSpecialEventSequence()
            for i in specialSeq:
                self.processSpecialEvents(i)
                self.device.shell('monkey -p ' + self.package + ' -vvv ' + str(self.number))
            return True
        except:
            return False

    def runnerSimpleEvents(self):
        """run self.number random simple events
        """
        try:
            self.device.shell('monkey -p ' + self.package + ' -vvv ' + str(self.number))
            return True
        except:
            return False

    def runnerSpecialEvents(self):
        """run self.number pieces of random special events
        """
        try:
            specialSeq = self.generateSpecialEventSequence()
            for i in specialSeq:
                self.processSpecialEvents(i)
            return True
        except:
            return False

    def dumpLog(self):
        log = self.logcat.dump(filterTuples=[('*', 'W')])
        log = log.split('\n')
        result = []
        for line in log:
            if self.package in line:
                result.append(line)
        return result
        #self.device.shell('logcat *:W | grep '+self.activity)

    def clearLog(self):
        return self.logcat.clear()

    def runner(self, mode='mix'):
        #log=open('HeissenbugTesterlog.txt', 'w')
        #logcat=subprocess.Popen(['adb','logcat', '*:W', '|', 'grep', self.package], stdout=log)
        self.clearLog()
        if mode == 'mix':
            result = self.runnerMixEvents()
        elif mode == 'special':
            result = self.runnerSpecialEvents()
        elif mode == 'simple':
            result = self.runnerSimpleEvents()
        return result, self.dumpLog()


if __name__ == '__main__':
    device = EMonkeyDevice()
    test = HeisenbugTester(device, package='com.android.gallery3d')
    result, log = test.runner()
    print log



