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

""" This module provides the pipeline design. A pipeline contains several
stages where each retrieves outputs from its previous stage and generate inputs
for its following stage. Each stage is defined as a PipelineComponent. A stage 
can generate arbitrary number of outputs given one input. PipelineParcel caches
these outputs issues to the next stage one at a time. A special signal (EOF)
will be passed down to all stages when the first stage no long produces any
further data. After the EOF is dispatched and processed by all stages, the
pipeline is completed.
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


class PipelineComponent:
    def next(self, obj):
        return PipelineParcel()

    def handleEOF(self):
        parcel = PipelineParcel()
        parcel.enqueue(Pipeline.EOF)
        return parcel


class Pipeline:
    EOF = []  # use a dummy object as a marker
    """ The pipeline of a number of components
    """

    def __init__(self):
        self.pl = []

    def execute(self):
        """ Start the pipeline, until the first stage returns no further data
        """
        first = self.pl[0]
        while True:
            parcel = first.next(None)
            # if the first stage returns an empty parcel, then we are 
            # almost done. Just pass down the EOF to every following stage
            if parcel.isEmpty():
                self._executeSingleStep(1, Pipeline.EOF)
                break
            while not parcel.isEmpty():
                self._executeSingleStep(1, parcel.dequeue())

    def _executeSingleStep(self, index, obj):
        """ Intended for internal use only
        index specifies which stage
        """
        if index >= len(self.pl):
            return None
        if obj == Pipeline.EOF:
            parcel = self.pl[index].handleEOF()
        else:
            parcel = self.pl[index].next(obj)
        while not parcel.isEmpty():
            nextObj = parcel.dequeue()
            self._executeSingleStep(index + 1, nextObj)

    def addStep(self, step):
        """ Add a step/stage to the pipeline
        """
        self.pl.append(step)
