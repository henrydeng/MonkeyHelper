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
# Xinye Lin
#
from MonkeyHelperReplayer import MonkeyHelperReplayer
from Pipeline import PipelineParcel, PipelineComponent
from HeisenbugInjector import SpecialEvent
from WifiAgent import WifiAgent
from Agents import CellularAgent


class HeisenbugReplayer(PipelineComponent):
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
