#!/usr/bin/python
import os, sys, re, inspect
#from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
# The EMonkeyHelper module is in the same folder but monkeyrunner launcher needs to know
#from EMonkeyHelper import EMonkeyDevice

def module_path():
    ''' returns the module path without the use of __file__.
    from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(os.path.dirname(inspect.getsourcefile(module_path)))
sys.path.append(module_path())
# the doc for the MT protocol can be found here:
# https://www.kernel.org/doc/Documentation/input/multi-touch-protocol.txt

# The parcel exchanged between different steps of a pipeline
class PipelineParcel:
    def __init__(self):
        self.q = []
    def enqueue(self, obj):
        self.q.append(obj)
    def dequeue(self):
        return self.q.pop(0)
    def isEmpty(self):
        return len(self.q) == 0

class MotionEvent:
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

class GeteventCommand:
    timestamp = 0
    evType = ""
    evCmd = ""
    evVal = 0
    def __str__(self):
        return str((self.timestamp, self.evType, self.evCmd, self.evVal))

# A Type A multi-touch screen
# a list of supported features:

class MultiTouchTypeAParser:
    NAVIGATION_HEIGHT = 48
    def __init__(self):
        self.currentSlot = None
        self.listMotions = []
    def next(self, geteventCmd):
        parcel = PipelineParcel()
        if geteventCmd.evType == "EV_ABS":
            if self.currentSlot is None:
                self.currentSlot = MotionEvent()
            if geteventCmd.evCmd == "ABS_MT_POSITION_X" or geteventCmd.evCmd == "ABS_X":
                self.currentSlot.x = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_POSITION_Y" or geteventCmd.evCmd == "ABS_Y":
                self.currentSlot.y = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_TRACKING_ID":
                self.currentSlot.tracking_id = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_PRESSURE":
                self.currentSlot.pressure = geteventCmd.evVal
            elif geteventCmd.evCmd == "ABS_MT_TOUCH_MAJOR":
                self.currentSlot.touch_major = geteventCmd.evVal
            else:
                print "[WARN] Type A MT meets unknown evCmd" + str(geteventCmd)
        elif geteventCmd.evType == "EV_KEY":
            if geteventCmd.evCmd == "BTN_TOUCH":
                print "[WARN] TypeA MT ignores BTN_TOUCH"
            else:
                print "[WARN] TYPEA MT meets unknown evCmd" + str(geteventCmd)
        elif geteventCmd.evType == "EV_SYN":
            if geteventCmd.evCmd == "SYN_REPORT":
                parcel.enqueue(self.listMotions)
                self.listMotions = []
                self.curentSlot = None
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
        

# A type B multi-touch screen
# a list of supported features:
# MT_PRESSURE, MT_POSITION_X, MT_POSITION_Y, TRACKING_ID, SLOT, TOUCH_MAJOR
# unsupported:
# ABS_MT_TOUCH_MINOR, ABS_MT_WIDTH_MAJOR, ABS_MT_WIDTH_MINOR, ABS_MT_DISTANCE
# ABS_MT_ORIENTATION, ABS_MT_TOOL_X, ABS_MT_TOOL_Y
class MultiTouchTypeBParser:
    NAVIGATION_HEIGHT = 48 # the standard navigation bar at the bottom
    def __init__(self):
        # states
        self.currentSlotIndex = 0
        self.currentSlot = MotionEvent()
        self.slots = [self.currentSlot]
    def next(self, geteventCmd):
        parcel = PipelineParcel()
        if geteventCmd.evType == "EV_ABS":
            if geteventCmd.evCmd == "ABS_MT_SLOT":
                self.currentSlotIndex = geteventCmd.evVal
                if geteventCmd.evVal >= len(self.slots):
                    self.slots.extend([None]*(geteventCmd.evVal + 1 - len(self.slots)))
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

# A generic printer, print whatever given
class GenericPrinter:
    def next(self, whatever):
        print str(whatever)
        return PipelineParcel()

# A text file reader which reads the file line by line
class TextFileLineReader:
    def __init__(self, tracePath):
        self.fp = open(tracePath)
    def next(self, dummy):
        parcel = PipelineParcel()
        line = self.fp.readline()
        if line != "":
            parcel.enqueue(line)
        return parcel        

# A trace parser for raw getevent trace
class RawTraceParser:
    def __init__(self):
        # a line is in the format of:
        # "time(float) evType(str) evCmd(str) evVal(int)"
        # refer to Linux evdev for details
        # here we assume the line is a readable dump from getevent
        self.pattern = re.compile("\\[\s*(\d+\.\d+)\\]\s*(\w+)\s*(\w+)\s*(\w+)")
    def next(self, line):
        m = self.pattern.match(line)
        e = GeteventCommand()
        e.timestamp = float(m.group(1))
        e.evType = m.group(2)
        e.evCmd = m.group(3)
        if m.group(4) == "DOWN":
            e.evVal = 1 # TODO special cases for BTN_TOUCH
        elif m.group(4) == "UP":
            e.evVal = 0
        else:
            e.evVal = int(m.group(4), 16)
        parcel = PipelineParcel()
        parcel.enqueue(e)
        return parcel

class FingerDecomposer:
    def __init__(self):
        self.tracker = {}
    def next(self, motionEvent):
        if motionEvent.tracking_id in self.tracker:
            self.tracker[motionEvent.tracking_id].append(motionEvent)
        else:
            self.tracker[motionEvent.tracking_id] = [motionEvent]
        return PipelineParcel()

class MonkeyHelperReplayer:
    def __init__(self):
        self.device = EMonkeyDevice()
        self.xValues=[]
        self.yValues=[]
        self.times=[]
        self.lastTimeStamp=0
        self.first=True
    def next(self, whatever):
        if len(whatever)==0:    #if it is empty
            if len(self.xValues)==1:
                if (self.first):
                    self.lastTimeStamp=self.times[0]
                    self.first=False
                else:
                    self.device.sleep(self.times[0]-self.lastTimeStamp)
                self.device.touch(self.xValues[0], self.yValues[0])
                print self.xValues[0], self.yValues[0]
                self.lastTimeStamp=self.times[0]
            else:
                self.first=False
                for count in range (len(self.xValues)):
                    if (count==0):
                        self.device.touch(self.xValues[0], self.yValues[0], MonkeyDevice.DOWN)
                        continue
                    self.device.sleep(self.times[count]-self.times[count-1])
                    self.device.touch(self.xValues[count], self.yValues[count], MonkeyDevice.MOVE)
                self.device.touch(self.xValues[len(self.xValues)-1], self.yValues[len(self.yValues)-1], MonkeyDevice.UP)
                self.lastTimeStamp=self.times[len(self.times)-1]
            self.xValues=[]
            self.yValues=[]
            self.times=[]
        else:
            next=whatever.pop(0)
            tempXValue=float(next.x)
            tempYValue=float(next.y)
            tempXValue=int(((tempXValue/1597)*1280)+0.5)
            tempYValue=int(((tempYValue/999)*800)+0.5)
            self.times.append(next.timestamp)
            self.xValues.append(tempXValue)
            self.yValues.append(tempYValue)
        return PipelineParcel()
        
class Pipeline:
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

def main():
    if len(sys.argv) <= 1:
        print "Usage: python test.py TRACE_PATH"
        print "The trace must be generated from getevent -lt [EVDEV]"
        return 1
    print ("timestamp", "tracking_id", "touch_major", "x", "y", "pressure")
    pl = Pipeline()
    pl.addStep(TextFileLineReader(sys.argv[1]))
    pl.addStep(RawTraceParser())
    pl.addStep(MultiTouchTypeAParser())
    # pl.addStep(FingerDecomposer())
    # pl.addStep(MonkeyHelperReplayer())
    pl.addStep(GenericPrinter())
    pl.execute()

if __name__ == "__main__":
    main()
