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

"""
This module provides a component to inject hesenbugs into the replay trace
"""

import random
from Pipeline import PipelineParcel, PipelineComponent
from MonkeyHelper import MonkeyHelperReplayer
from Agents import CellularAgent, WifiAgent


class SpecialEvent:
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp

    def getTimeStamp(self):
        return self.timestamp

    def getName(self):
        return self.name

    def setTimeStamp(self, timestamp):
        self.timestamp = timestamp

    def setName(self, name):
        self.name = name


class TroubleInjector(PipelineComponent):
    """Inject random events into the replay trace,
    the randomness of these events are controlled by a seed, thus reproducible
    """

    def __init__(self, seed='WTF', specialEvents=['wifi', 'cellular'], number=25):
        """SpecialEvents is a list containing the names of all possible special events.
            current possible special events:
                wifi
                cellular

        """
        random.seed(seed)
        seq=specialEvents * (number/len(specialEvents)+1)
        self.randomSeries = random.sample(seq, number)
        self.insertChoice=[]
        while self.insertChoice.count(True)<number:
            self.insertChoice.extend(random.sample([True,False],1))
        self.prevTrail = None
        self.idx = 0
        self.insertionIdx=0
        self.parcel = PipelineParcel()

    def next(self, trail):
        """read in the trails and inject special events
        """
        if self.prevTrail:
            if self.idx <= len(self.randomSeries):
                if self.insertChoice[self.insertionIdx]:
                    timestamp = (self.prevTrail[0].timestamp + trail[0].timestamp) / 2
                    injection = SpecialEvent(self.randomSeries[self.idx], timestamp)
                    self.parcel.enqueue(injection)
                    self.idx = self.idx + 1
                else:
                    pass
                self.insertionIdx=self.insertionIdx+1
            else:
                pass
        else:
            pass
        self.parcel.enqueue(trail)
        self.prevTrail = trail
        return PipelineParcel()

    def handleEOF(self):
        return self.parcel
    

class TroubleReplayer(PipelineComponent):
    """Replay finger trails with Heisenbug events injected in between
    """

    def __init__(self):
        self.mReplayer = MonkeyHelperReplayer()
        self.device = self.mReplayer.device
        self.lastTimeStamp = 0
        self.wifiAgent = WifiAgent(self.device)
        self.cellularAgent = CellularAgent(self.device)

    def next(self, trail):
        if not isinstance(trail, SpecialEvent):
            self.mReplayer.lastTimeStamp = self.lastTimeStamp
            parcel = self.mReplayer.next(trail)
            self.lastTimeStamp = self.mReplayer.lastTimeStamp
            return parcel
        else:
            name = trail.getName()
            lastTimeStamp = self.lastTimeStamp
            if trail.getTimeStamp()>lastTimeStamp:
                self.device.sleep(trail.getTimeStamp() - lastTimeStamp)
            else:
                pass
            if name == 'wifi':
                print 'Injecting wifi event'
                self.wifiAgent.changeWifiStatus()
            elif name == 'cellular':
                self.cellularAgent.toggleCellularDataStatus()
                print 'Injecting cellular event'
            self.lastTimeStamp = trail.getTimeStamp()
            return PipelineParcel()
