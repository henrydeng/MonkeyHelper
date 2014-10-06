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
#   Mingyuan Xia
#   Ran Shu
#

class SnapshotAgent :
    def __init__(self, device):
        self.device = device
        
    def takeSnapshot(self):
        ''' Return a snapshot object
        '''
        return self.device.takeSnapshot()
    
    def saveSnapshot(self, snapshot, fileName):
        ''' Save a snapshot object to a png file
        '''
        snapshot.writeToFile(fileName,'png')
        
    def compareSnapshots(self, snapshot1, snapshot2):
        ''' Check if two snapshot objects are the same
        '''
        return snapshot1.sameAs(snapshot2, 1)

    def takeAndCompareSnapshots(self, snapshotCheck):
        ''' Take a snapshot and check if it is the same as another one
        '''
        return self.compareSnapshots(self.takeSnapshot(), snapshotCheck)
        
    def getSubSnapshot(self, snapshot, coordinates):
        ''' Get a region from a snapshort
        '''
        return snapshot.getSubImage(coordinates)
    
    def loadSnapshot (self, fileName):
        ''' Load a snapshot object from a png file
        '''
        return self.device.loadImageFromFile(fileName)
