#!/usr/bin/python
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
#

""" This module provides the facilities to support component based design
"""

class PipelineParcel:
    """ The parcel exchanged between different steps of a pipeline
    """
    def __init__(self):
        self.q = []
    def enqueue(self, obj):
        self.q.append(obj)
    def dequeue(self):
        return self.q.pop(0)
    def isEmpty(self):
        return len(self.q) == 0
   
class Pipeline:
    """ The pipeline of a number of components
    """
    def __init__(self):
        self.pl = []
    def execute(self):
        first = self.pl[0]
        while True:
            parcel = first.next(None)
            if parcel.isEmpty():
                break
            while not parcel.isEmpty():
                obj = parcel.dequeue()
                self._executeSingleStep(1, obj)
    def _executeSingleStep(self, index, obj):
        if index >= len(self.pl):
            return None
        parcel = self.pl[index].next(obj)
        while not parcel.isEmpty():
            nextObj = parcel.dequeue()
            self._executeSingleStep(index+1, nextObj)
    def addStep(self, step):
        self.pl.append(step)
