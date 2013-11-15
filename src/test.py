#!/usr/bin/python
# from MonkeyHelper import MonkeyHelper 
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# starting the application and test
print "Starting the monkeyrunner script"

# MonkeyHelper.aapt_dump("1.apk")

# connection to the current device, and return a MonkeyDevice object
device = MonkeyRunner.waitForConnection()

#screenshot
MonkeyRunner.sleep(1)

#sending an event which simulate a click on the menu button
device.drag ( (95,400), (540,400), 0.05, 100)
MonkeyRunner.sleep(1)
device.drag ( (540,400), (95,400), 0.05, 100)
MonkeyRunner.sleep(1)
device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)

print "Finishing the test"
