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
#   Ran Shu
#

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
"""
If taking a screenshot, use this block of code and comment out line 25
monkeyImage1=device.takeSnapshot()
monkeyImage1.writeToFile('screen_shot1.png','png')
"""
monkeyImage1 = MonkeyRunner.loadImageFromFile('screen_shot1.png')
monkeyImage2 = MonkeyRunner.loadImageFromFile('screen_shot2.png')
#Comparing an image with itself
if monkeyImage1.sameAs(monkeyImage1, 1):
    print "1st Test: match"
else:
    print "1st Test: not a match"
#Comparing two similar images, not a match with 0.9, where 90% of the pixels must match
if monkeyImage1.sameAs(monkeyImage2, 0.9):
    print "2nd Test: match"
else:
    print "2nd Test: not a match"
#Comparing two similar images, the two images are a match with 0.8, where 80% of the pixels must match
if monkeyImage1.sameAs(monkeyImage2, 0.8):
    print "3rd Test: match"
else:
    print "3rd Test: not a match"

#Trying to match subImages
subimage1 = monkeyImage1.getSubImage((110, 100, 260, 100))
subimage1.writeToFile('subimage1.png', 'png')
subimage2 = monkeyImage2.getSubImage((110, 100, 260, 100))
subimage2.writeToFile('subimage2.png', 'png')

if subimage1.sameAs(subimage2, 0.8):
    print "4th Test: match"
else:
    print "4th Test: not a match"
