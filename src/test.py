#!/usr/bin/python
import os, sys, inspect
def module_path():
    ''' returns the module path without the use of __file__.
    from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(os.path.dirname(inspect.getsourcefile(module_path)))
sys.path.append(module_path())

# The MonkeyHelper module is in the same folder but monkeyrunner launcher needs to know
from MonkeyHelper import EMonkeyDevice 
from com.android.monkeyrunner import MonkeyRunner

# starting the application and test
print "Starting the monkeyrunner script"

# MonkeyHelper.aapt_dump("1.apk")

# automatically connect to the current device
device = EMonkeyDevice()

MonkeyRunner.sleep(1)
# slide right
device.drag ( (95,400), (540,400), 0.05, 100)
MonkeyRunner.sleep(1)
# slide left
device.drag ( (540,400), (95,400), 0.05, 100)
MonkeyRunner.sleep(1)
# press the menu key
device.press('KEYCODE_MENU', EMonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(1)
device.touch( 95, 400, EMonkeyDevice.DOWN_AND_UP)

print "Finishing the test"
