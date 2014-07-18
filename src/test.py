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
#   Ran Shu
#

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
