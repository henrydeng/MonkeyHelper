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

"""
This script capture several live scrolling gesture and learn user's scrolling
speed. Then it produces further scrolling at user's pace.
"""

import os, sys, inspect
def module_path():
    ''' returns the module path without the use of __file__.
    from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(os.path.dirname(inspect.getsourcefile(module_path)))
sys.path.append(module_path())

from Pipeline import Pipeline, PipelineParcel
import TraceManipulation as dtm
from MonkeyHelper import EMonkeyDevice
import subprocess, signal

class LiveGeteventReader(PipelineComponent):
    def __init__(self):
        cmd = '/Applications/android-sdk-macosx/platform-tools/adb shell getevent -lt /dev/input/event1'
        self.p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.mustTerminate = False
    def next(self, dummy):
        parcel = PipelineParcel()
        line = self.p.stdout.readline()
        if self.mustTerminate or (line == '' and self.p.poll() != None):
            return parcel
        parcel.enqueue(line)
        return parcel
    def terminate(self):
        # not available on Jython 2.53 (with monkeyrunner of Android SDK)
        # self.p.terminate()
        # has to do this, with a process leak
        self.mustTerminate = True

class AutoScrollingLearner(PipelineComponent):
    def __init__(self, reader, sample_count):
        self.reader = reader
        self.sample_count = sample_count
        self.samples = []
        self.lastTimestamp = 0
        self.stats = None
    def next(self, trail):
        pointCount = len(trail)
        duration = trail[len(trail)-1].timestamp - trail[0].timestamp
        xdelta = trail[len(trail)-1].x - trail[0].x
        ydelta = trail[len(trail)-1].y - trail[0].y
        waitTime = trail[0].timestamp - self.lastTimestamp
        self.lastTimestamp = trail[len(trail)-1].timestamp
        sample = (waitTime, xdelta, ydelta, duration, pointCount)
        self.samples.append(sample)
        print sample
        self.sample_count -= 1 
        if self.sample_count == 0: 
            print "learning finished, do statistics"
            self.reader.terminate()
            count = len(self.samples)
            total = (0, 0, 0, 0, 0)
            for (_1, _2, _3, _4, _5) in self.samples:
                total = (total[0] + _1, total[1] + _2, total[2] + _3, total[3] + _4, total[4] + _5)
            self.stats = (total[0] / count, total[1] / count, total[2] / count, total[3] / count, total[4] / count)
            print self.stats
        return PipelineParcel()
    def getSpeedAndDelta(self):
        return self.stats
    
def main():
    # capture three samples and automatically scrolls five times
    SAMPLE_COUNT = 3
    REPEAT_COUNT = 5
    print "learning the pace of scrolling"
    pl = Pipeline()
    reader = LiveGeteventReader()
    pl.addStep(reader)
    pl.addStep(dtm.RawTraceParser())
    pl.addStep(dtm.MultiTouchTypeAParser())
    pl.addStep(dtm.RelativeTimingConverter())
    pl.addStep(dtm.FingerDecomposer())
    learner = AutoScrollingLearner(reader, SAMPLE_COUNT)
    pl.addStep(learner)
    pl.execute()
    (waitTime, xdelta, ydelta, duration, pointCount) = learner.getSpeedAndDelta()
    print "User scrolling parameters learned"
    device = EMonkeyDevice()
    (xmiddle, ymiddle) = (device.displayWidth / 2, device.displayHeight / 2)
    start = (xmiddle - xdelta/2, ymiddle - ydelta/2)
    end = (xmiddle + xdelta/2, ymiddle + ydelta/2)
    for _ in range(REPEAT_COUNT):
        device.sleep(waitTime)
        device.drag(start, end, duration, pointCount)
 
if __name__ == "__main__":
    main()
