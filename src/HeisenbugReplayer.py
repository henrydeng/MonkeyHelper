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
from MonkeyHelper import EMonkeyDevice
from Pipeline import PipelineParcel, PipelineComponent
from HeisenbugInjecter import SpecialEvent
from WifiAgent import WifiAgent
from CellularAgent import CellularAgent


class HeisenbugReplayer(PipelineComponent):
    """Replay finger trails with Heisenbug events injected in between
    """
    mReplayer = MonkeyHelperReplayer()

    def __init__(self):
        self.device = EMonkeyDevice()
        self.lastTimeStamp = 0
        self.wifiAgent = WifiAgent(self.device)
        self.cellularAgent = CellularAgent(self.device)

    def next(self, trail):
        if not isinstance(trail, SpecialEvent):
            self.mReplayer.lastTimeStamp = self.lastTimeStamp
            parcel = self.mReplayer.next(trail);
            self.lastTimeStamp = self.mReplayer.lastTimeStamp
            print 'here'
            return parcel
        else:
            name = trail.getName()
            lastTimeStamp = self.lastTimeStamp
            if name == 'wifi':
                self.device.sleep(trail.getTimeStamp() - lastTimeStamp)
                self.wifiAgent.changeWifiStatus()
                self.lastTimeStamp = trail.getTimeStamp()
            elif name == 'celluar':
                self.device.sleep(trail.getTimeStamp() - lastTimeStamp)
                self.cellularAgent.changeCellularDataStatus()
                self.lastTimeStamp = trail.getTimeStamp()
            return PipelineParcel()
