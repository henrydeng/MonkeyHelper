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
#   Mingyuan Xia
#


from Pipeline import PipelineComponent, PipelineParcel, Pipeline

class Replayer(PipelineComponent):
    def canAccept(self, replayEvent):
        """ Return True if the replayer can process this replay event
        """
        return False
    def next(self, replayEvent):
        """ Process the replay event and return a parcel like other
        pipeline components
        """
        return PipelineParcel()
    def getTimestamp(self):
        return self.timestamp
    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

class CompositeReplayer(Replayer):
    def __init__(self, replayers):
        self.replayers = replayers
    def next(self, replayEvent):
        for r in self.replayers:
            if r.canAccept(replayEvent):
                pp = r.next(replayEvent)
                # sync all timestamps
                for rp in self.replayers:
                    rp.setTimestamp(r.getTimestamp())
                return pp
        pp = PipelineParcel()
        pp.enqueue(replayEvent)
        return pp
    def canAccept(self, replayEvent):
        for r in self.replayers:
            if r.canAccept(replayEvent):
                return True
        return False
    def handleEOF(self): # TODO
        pp = PipelineParcel()
        pp.enqueue(Pipeline.EOF)
        return pp

class ReplayEvent:
    def __init__(self, timestamp):
        self.timestamp = timestamp

