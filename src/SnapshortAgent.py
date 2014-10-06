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
#   Ran Shu
#

# Imports the monkeyrunner module used by this program
from MonkeyHelper import EMonkeyDevice


class SnapshortAgent:
    def __init__(self):
        self.device = EMonkeyDevice()

    def takeSnapshot(self):
        snapshot = self.device.takeSnapshot()
        return snapshot

    def saveSnapshot(self, snapshot, fileName):
        snapshot.writeToFile(fileName + '.png', 'png')

    def compareSnapshots(self, snapshot1, snapshot2):
        return snapshot1.sameAs(snapshot2, 1)

    def takeAndCompareSnapshots(self, snapshotCheck):
        currentSnapshot = self.device.takeSnapshot()
        return self.compareSnapshots(currentSnapshot, snapshotCheck)

    def getSubSnapshot(self, snapshot, coordinates):
        subsnapshot = snapshot.getSubImage(coordinates)
        return subsnapshot

    def loadSnapshot(self, fileName):
        snapshot = self.device.loadImageFromFile(fileName)
        return snapshot
