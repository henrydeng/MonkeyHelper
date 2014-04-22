#!/usr/bin/python
import os, sys, inspect
def module_path():
    ''' returns the module path without the use of __file__.
    from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(os.path.dirname(inspect.getsourcefile(module_path)))
sys.path.append(module_path())

# The MonkeyHelper module is in the same folder but monkeyrunner launcher needs to know
from MonkeyHelper import EMonkeyDevice 

# starting the application and test
print "Starting the monkeyrunner script"

# MonkeyHelper.aapt_dump("1.apk")

# automatically connect to the current device
device = EMonkeyDevice()
print device.getInstalledPackage()
device.wake().sleep(1).unlockScreen().sleep(1)
device.slideRight().sleep(2).slideLeft().sleep(1)
device.press('KEYCODE_MENU').sleep(1).touch(95, 400).sleep(1)

print "Finishing the test"
