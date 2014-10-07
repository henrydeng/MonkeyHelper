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
from Agents import CellularAgent, WifiAgent
from Replayer import Replayer, ReplayEvent

class SpecialEvent(ReplayEvent):
    def __init__(self, name, timestamp):
        ReplayEvent.__init__(self, timestamp)
        self.name = name

    def getName(self):
        return self.name

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
        self.prevGesture = None
        self.idx = 0
        self.insertionIdx=0
        self.parcel = PipelineParcel()

    def next(self, gestureEvent):
        """read in the trails and inject special events
        """
        if self.prevGesture:
            if self.idx <= len(self.randomSeries):
                if self.insertChoice[self.insertionIdx]:
                    timestamp = (self.prevGesture.timestamp + gestureEvent.timestamp) / 2
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
        self.parcel.enqueue(gestureEvent)
        self.prevGesture = gestureEvent
        return PipelineParcel()

    def handleEOF(self):
        return self.parcel
    

class TroubleReplayer(Replayer):
    """Replay finger trails with Heisenbug events injected in between
    """

    def __init__(self, dev):
        Replayer.__init__()
        self.device = dev
        self.wifiAgent = WifiAgent(self.device)
        self.cellularAgent = CellularAgent(self.device)

    def next(self, specialEvent):
        name = specialEvent.getName()
        lastTimeStamp = self.getTimestamp()
        if specialEvent.timestamp>lastTimeStamp:
            self.device.sleep(specialEvent.timestamp - lastTimeStamp)
        else:
            pass
        if name == 'wifi':
            print 'Injecting wifi event'
            self.wifiAgent.changeWifiStatus()
        elif name == 'cellular':
            self.cellularAgent.toggleCellularDataStatus()
            print 'Injecting cellular event'
        self.setTimestamp(specialEvent.timestamp)
        return PipelineParcel()
    
    def canAccept(self, replayEvent):
        return isinstance(replayEvent, SpecialEvent)
