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
import random
from WifiAgent import WifiAgent
from CellularAgent import CellularAgent
import subprocess

class Heisenbug:

    def __init__(self,device,package,seed=11,number=10):
        self.device=device
        self.seed=seed
        self.number=number
        self.package=package
        #TODO add orientation and other events
        self.specialEvents=['wifi','data']
        random.seed(self.seed)

    def generateSpecialEventSequence(self):
        length=len(self.specialEvents)
        seq=self.specialEvents*(self.number/length)
        length=len(seq)
        if length<self.number:
            seq=seq+seq[0:self.number-length]
        elif length>self.number:
            seq=seq[0:self.number]
        seq=random.sample(seq,self.number)
        return seq

    def processSpecialEvents(self,specialEvent):
        if specialEvent=='wifi':
            WifiAgent(self.device).changeWifiStatus()
        elif specialEvent=='data':
            CellularAgent(self.device).changeCellularDataStatus()


    def runnerMixEvents(self):
        """run self.number random special events
           and self.number random simple events in between of any two continuous special events
        """
        try:
            specialSeq=self.generateSpecialEventSequence()
            for i in specialSeq:
                self.processSpecialEvents(i)
                self.device.shell('monkey -p '+self.package+' -vvv '+str(self.number))
            return True
        except:
            return False

    def runnerSimpleEvents(self):
        """run self.number random simple events
        """
        try:
            self.device.shell('monkey -p '+self.package+' -vvv '+str(self.number))
            return True
        except:
            return False

    def runnerSpecialEvents(self):
        """run self.number random special events
        """
        try:
            specialSeq=self.generateSpecialEventSequence()
            for i in specialSeq:
                self.processSpecialEvents(i)
            return True
        except:
            return False

    def runnerLog(self):
        self.device.shell('logcat *:W | grep '+self.activity)

    def runner(self,type='mix'):
        log=open('log.txt', 'w')
        logcat=subprocess.Popen(['adb','logcat', '*:W', '|', 'grep', self.package], stdout=log)
        if type=='mix':
            result=self.runnerMixEvents()
        elif type=='special':
            result=self.runnerSimpleEvents()
        elif type=='simple':
            result=self.runnerSimpleEvents()
        #TODO kill the subprocess, logcat.kill() and logcat.terminate() cannot work due to Jython
        #logcat.terminate()
        log.close()
        return result

if __name__=='__main__':
    device=MonkeyRunner.waitForConnection()
    test=Heisenbug(device,package='com.android')
    test.runner()


