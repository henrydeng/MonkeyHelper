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

"""
This module provides several components that can manipulate the trace
collected from Android devices. 
"""

import re, sys
from Pipeline import PipelineParcel, PipelineComponent


class MotionEvent:
    """ This data structure describes a single evdev report
    """
    timestamp = 0
    tracking_id = 0xFFFFFFFF
    touch_major = 0
    x = 0
    y = 0
    pressure = 0

    def __str__(self):
        return str((self.timestamp, self.tracking_id, self.touch_major, self.x, self.y, self.pressure))

    def __repr__(self):
        return self.__str__()

    def clone(self):
        s = MotionEvent()
        s.timestamp = self.timestamp
        s.tracking_id = self.tracking_id
        s.touch_major = self.touch_major
        s.x = self.x
        s.y = self.y
        s.pressure = self.pressure
        return s


class GeteventCommand:
    """ This data structure describes a single command from Android getevent utility
    """
    timestamp = 0
    evType = ""
    evCmd = ""
    evVal = 0

    def __str__(self):
        return str((self.timestamp, self.evType, self.evCmd, self.evVal))


# the doc for the MT protocol can be found here:
# https://www.kernel.org/doc/Documentation/input/multi-touch-protocol.txt

class MultiTouchTypeAParser(PipelineComponent):
    """ A type-A multi-touch evdev device
    """
    NAVIGATION_HEIGHT = 48  # the height of the standard navigation bar at the bottom, in pixels

    def __init__(self):
        self.currentSlot = MotionEvent()
        self.listMotions = []
        self.dontReport = False  # one-shot disabler

    def next(self, geteventCmd):
        """ Take a stream of getevent commands and produce motion events
        """
        parcel = PipelineParcel()
        if geteventCmd.evType == "EV_ABS":
            if self.currentSlot is None:
                self.currentSlot = MotionEvent()
            if geteventCmd.evCmd == "ABS_MT_POSITION_X" or geteventCmd.evCmd == "ABS_X":
                self.currentSlot.x = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_POSITION_Y" or geteventCmd.evCmd == "ABS_Y":
                self.currentSlot.y = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_TRACKING_ID":
                if geteventCmd.evVal == 0xFFFFFFFF:
                    self.currentSlot = None
                else:
                    self.currentSlot.tracking_id = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_PRESSURE":
                self.currentSlot.pressure = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_TOUCH_MAJOR":
                self.currentSlot.touch_major = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MISC":
                self.dontReport = True
            else:
                print "[WARN] Type A MT meets unknown evCmd" + str(geteventCmd)
        elif geteventCmd.evType == "EV_KEY":
            if geteventCmd.evCmd == "BTN_TOUCH":
                print "[WARN] TypeA MT ignores BTN_TOUCH"
            else:
                print "[WARN] TYPEA MT meets unknown evCmd" + str(geteventCmd)
        elif geteventCmd.evType == "EV_SYN":
            if geteventCmd.evCmd == "SYN_REPORT":
                if self.currentSlot is not None:
                    self.currentSlot.timestamp = geteventCmd.timestamp
                    self.listMotions.append(self.currentSlot)
                    self.currentSlot = self.currentSlot.clone()
                if self.dontReport:
                    self.dontReport = False
                else:
                    parcel.enqueue(self.listMotions)
                self.listMotions = []
            elif geteventCmd.evCmd == "SYN_MT_REPORT":
                if self.currentSlot is not None:
                    self.currentSlot.timestamp = geteventCmd.timestamp
                    self.listMotions.append(self.currentSlot)
                    self.currentSlot = None
            else:
                print "[WARN] Type A MT meets unknown evCmd" + str(geteventCmd)
        else:
            print "[WARN] Type A MT skips unknown line:" + str(geteventCmd)
        return parcel


class MultiTouchTypeBParser(PipelineComponent):
    """ A type-B multi-touch screen
    a list of supported features:
    MT_PRESSURE, MT_POSITION_X, MT_POSITION_Y, TRACKING_ID, SLOT, TOUCH_MAJOR
    unsupported:
    ABS_MT_TOUCH_MINOR, ABS_MT_WIDTH_MAJOR, ABS_MT_WIDTH_MINOR, ABS_MT_DISTANCE
    ABS_MT_ORIENTATION, ABS_MT_TOOL_X, ABS_MT_TOOL_Y
    """
    NAVIGATION_HEIGHT = 48  # the standard navigation bar at the bottom

    def __init__(self):
        # states
        self.currentSlotIndex = 0
        self.currentSlot = MotionEvent()
        self.slots = [self.currentSlot]

    def next(self, geteventCmd):
        """ Takes a stream of getevent commands and produce motion events
        """
        parcel = PipelineParcel()
        if geteventCmd.evType == "EV_ABS":
            if geteventCmd.evCmd == "ABS_MT_SLOT":
                self.currentSlotIndex = geteventCmd.evVal
                if geteventCmd.evVal >= len(self.slots):
                    self.slots.extend([None] * (geteventCmd.evVal + 1 - len(self.slots)))
                    self.slots[geteventCmd.evVal] = MotionEvent()
                self.currentSlot = self.slots[self.currentSlotIndex]
            elif geteventCmd.evCmd == "ABS_MT_POSITION_X":
                self.currentSlot.x = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_POSITION_Y":
                self.currentSlot.y = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_TRACKING_ID":
                if geteventCmd.evVal == 0xFFFFFFFF:
                    # unbinding
                    self.slots[self.currentSlotIndex] = MotionEvent()
                else:
                    # binding tracking_id to slot
                    self.currentSlot.tracking_id = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_PRESSURE":
                self.currentSlot.pressure = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_TOUCH_MAJOR":
                self.currentSlot.touch_major = geteventCmd.evVal
            else:
                print "[WARN] Type B MT meets unknown evCmd" + str(geteventCmd)
        elif geteventCmd.evType == "EV_SYN":
            if geteventCmd.evCmd == "SYN_REPORT":
                for motionEvent in self.slots:
                    if motionEvent.tracking_id != 0xFFFFFFFF:
                        motionEvent.timestamp = geteventCmd.timestamp
                        parcel.enqueue(motionEvent)
            else:
                print "[WARN] Type B MT meets unknown evCmd" + str(geteventCmd)
        else:
            print "[WARN] Type B MT skips unknown line:" + str(geteventCmd)
        return parcel


class GenericPrinter(PipelineComponent):
    """ A generic printer, print whatever given
    """

    def next(self, whatever):
        """ Takes whatever object and print its string representation
        """
        print str(whatever)
        return PipelineParcel()


class TextFileLineReader(PipelineComponent):
    """ A text file reader which reads the file line by line
    """

    def __init__(self, tracePath):
        self.fp = open(tracePath)

    def next(self, dummy):
        """ Takes nothing and produces lines from the file
        """
        parcel = PipelineParcel()
        line = self.fp.readline()
        if line != "":
            parcel.enqueue(line)
        return parcel


class RawTraceParser(PipelineComponent):
    """ A trace parser for raw getevent traces
    """

    def __init__(self):
        self.pattern = re.compile("\\[\s*(\d+\.\d+)\\]\s*(\w+)\s*(\w+)\s*(\w+)")

    def next(self, line):
        """ Takes a single line of the raw trace and produces a getevent command object
        a line is in the format of:
        time(float) evType(str) evCmd(str) evVal(int)
        refer to the Linux evdev doc for details
        here we assume the line is dumped from `getevent -lt <EVDEV>
        """
        m = self.pattern.match(line)
        e = GeteventCommand()
        if m is None:
            print "[ERROR] unidentified raw trace line:" + line
            sys.exit()
        e.timestamp = float(m.group(1))
        e.evType = m.group(2)
        e.evCmd = m.group(3)
        if m.group(4) == "DOWN":
            e.evVal = 1  # TODO special cases for BTN_TOUCH
        elif m.group(4) == "UP":
            e.evVal = 0
        else:
            e.evVal = int(m.group(4), 16)
        parcel = PipelineParcel()
        parcel.enqueue(e)
        return parcel


class FingerDecomposer(PipelineComponent):
    """ Decompose motion event stream into finger trails
    """

    def __init__(self):
        self.tracker = {}

    def next(self, listMotionEvents):
        """ Takes a list of motion events and produces finger trails
        """
        prev = self.tracker
        alive = {}
        for e in listMotionEvents:
            if e.tracking_id in prev:
                t = prev[e.tracking_id]
                t.append(e)
                del prev[e.tracking_id]
                alive[e.tracking_id] = t
            else:
                alive[e.tracking_id] = [e]
        self.tracker = alive
        parcel = PipelineParcel()
        for specialEvent in prev.values():
            parcel.enqueue(specialEvent)
        return parcel


class TrailScaler(PipelineComponent):
    """ Scale the coordinates of the motion events in the trail
    Used to adapt the trail from one device to another with a different resolution
    """

    def __init__(self, xfactor, yfactor):
        self.xfactor = xfactor
        self.yfactor = yfactor

    def scaleXY(self, motionEvent):
        tempXValue = float(motionEvent.x)
        tempYValue = float(motionEvent.y)
        tempXValue = int((tempXValue * self.xfactor) + 0.5)
        tempYValue = int((tempYValue * self.yfactor) + 0.5)
        motionEvent.x = tempXValue
        motionEvent.y = tempYValue

    def next(self, specialEvent):
        """ Takes a specialEvent and produces a scaled specialEvent with given factors
        """
        for e in specialEvent:
            self.scaleXY(e)
        parcel = PipelineParcel()
        parcel.enqueue(specialEvent)
        return parcel


class TimeScaler(PipelineComponent):
    """ Scale the time of a trail, e.g. accelerate/decelerate the replaying
    """

    def __init__(self, factor):
        self.factor = factor

    def next(self, specialEvent):
        """ Takes a specialEvent and produces a time-scaled specialEvent
        """
        for e in specialEvent:
            e.timestamp *= self.factor
        parcel = PipelineParcel()
        parcel.enqueue(specialEvent)
        return parcel


class RelativeTimingConverter(PipelineComponent):
    """ Convert all timestamp based on the first one in the trace
    """
    baseTimestamp = None

    def next(self, listMotionEvents):
        if self.baseTimestamp is None:
            self.baseTimestamp = listMotionEvents[0].timestamp
        for e in listMotionEvents:
            e.timestamp -= self.baseTimestamp
        parcel = PipelineParcel()
        parcel.enqueue(listMotionEvents)
        return parcel
