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
#   Ran Shu
#

""" This module provides a component to replay the trace to an Android device
via MonkeyHelper interfaces.
"""
from MonkeyHelper import EMonkeyDevice
from Pipeline import PipelineParcel, PipelineComponent


class MonkeyHelperReplayer(PipelineComponent):
    """ Replay finger trails to an Android box via MonkeyHelper interfaces
    """

    def __init__(self):
        self.device = EMonkeyDevice()
        self.lastTimeStamp = 0

    def next(self, trail):
        """ Takes a finger trail and produces nothing
        """
        lastTimeStamp = self.lastTimeStamp
        if len(trail) <= 0:
            print "[WARN] perform an empty trail"
        elif len(trail) == 1:
            actions = [EMonkeyDevice.DOWN_AND_UP]
        else:
            actions = [EMonkeyDevice.DOWN] + [EMonkeyDevice.MOVE] * (len(trail) - 2) + [EMonkeyDevice.UP]
        for count in range(len(trail)):
            self.device.sleep(trail[count].timestamp - lastTimeStamp)
            self.device.touch(trail[count].x, trail[count].y, actions[count])
            lastTimeStamp = trail[count].timestamp
        self.lastTimeStamp = lastTimeStamp
        return PipelineParcel()
