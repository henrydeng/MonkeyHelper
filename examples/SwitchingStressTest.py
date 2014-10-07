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

""" This test will repeatedly launch and switch apps, which serve
as a stress test for the life cycle methods of the main activity of
the app being tested.
"""

import os, sys, inspect


def module_path():
    ''' returns the module path without the use of __file__.
    from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(os.path.dirname(inspect.getsourcefile(module_path)))


sys.path.append(module_path())
sys.path.append(os.path.join(module_path(), '..', 'src'))

from MonkeyHelper import EMonkeyDevice
from Agents import LogcatAgent
import time


def main():
    """ This test launches a series of apps (with given package and main activity names)
    and repeats this for a given number of times. After that, the scripts dumps the error
    messages printed to logcat during the test.
    """
    # constants
    APP_HOME = 'com.android.launcher/com.android.launcher2.Launcher'
    APP_CLOCK = 'com.google.android.deskclock/com.android.deskclock.DeskClock'
    # configurations
    packages = [APP_CLOCK, APP_HOME]
    sleep_interval = 2
    repeats = 2
    app_tag = 'ActivityManager'
    device = EMonkeyDevice()
    agent = LogcatAgent(device)
    agent.clear()
    print 'Start launching stress test'
    for _ in range(repeats):
        for p in packages:
            device.startActivity(component=p)
            time.sleep(sleep_interval)
    err = agent.dump(fmt=None, filterTuples=[(app_tag, 'E'), ('*', 'S')])
    print 'Finishing test, dumping error messages:'
    print err


main()