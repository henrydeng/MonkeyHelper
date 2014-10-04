#
# Copyright 2014 Mingyuan Xia (http://mxia.me) and others
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

"""
This module provides a component to inject hesenbugs into the replay trace
"""

import random
from Pipeline import PipelineParcel,PipelineComponent

class SpecialEvent:
    def __init__(self,name,timestamp):
        self.name=name
        self.timestamp=timestamp
    def getTimeStamp(self):
        return self.timestamp
    def getName(self):
        return self.name
    def setTimeStamp(self,timestamp):
        self.timestamp=timestamp
    def setName(self,name):
        self.name=name


class HeisenbugInjecter(PipelineComponent):
    """Inject random events into the replay trace,
    the ransomness of these events are controlled by a seed, thus reproducible
    """

    def __init__(self,seed,SpecialEvents,number):
        """SpecialEvents is a list containing the names of all the possible special events
        current possible special events:
            wifi
            cellular

        """
        random.seed=seed
        self.randomSeries=random.sample(SpecialEvents,number)
        self.insertChoice=random.sample([True,False],number)
        self.prevTrail=None
        self.idx=0
        self.parcel=PipelineParcel()

    def next(self,trail):
        """read in the trails and inject special events
        """
        if self.prevTrail:
            self.parcel.enqueue(trail)
            if self.idx<=len(self.randomSeries):
                if self.insertChoice[self.idx]:
                    timestamp=(self.prevTrail.timestamp+trail.timestamp)/2
                    injection=SpecialEvent(self.randomSeries[self.idx],timestamp)
                    self.parcel.enqueue(injection)
                    self.idx=self.idx+1
            self.prevTrail=trail

    def handleEOF(self):
        return self.parcel
