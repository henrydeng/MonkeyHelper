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

from Pipeline import Pipeline
import TraceManipulation as dtm
from MonkeyHelperReplayer import MonkeyHelperReplayer
from MonkeyHelper import MonkeyHelper, EMonkeyDevice, _cmd
import subprocess

def main():
    print "learning the pace of scrolling"
    device = EMonkeyDevice()
    # cmd = ["adb", "shell", "getevent", "-lt"]
    cmd = ["adb", "shell", "logcat"]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, 
                stderr = subprocess.PIPE)
    for line in p.stdout:
        print line
        
if __name__ == "__main__":
    main()
