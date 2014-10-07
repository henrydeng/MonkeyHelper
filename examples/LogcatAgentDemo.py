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
# Contributor(s):
#   Mingyuan Xia
#

""" This script demonstrates how to read the logcat output from a device. You need
monkeyrunner to run scripts once including this module
"""

import os, sys, inspect


def module_path():
    ''' returns the module path without the use of __file__.
    from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(os.path.dirname(inspect.getsourcefile(module_path)))


sys.path.append(module_path())

import MonkeyHelper as mh
import LogcatAgent as la
import time


def main():
    """ This example dumps all error messages in logcat and then clear it.
    After 5 seconds, it dumps all messages and finishes.
    Note that logcat encodes its output with utf-8
    """
    device = mh.EMonkeyDevice()
    agent = la.LogcatAgent(device)
    print agent.dump(fmt=None, filterTuples=[('*', 'E')])
    agent.clear()
    print 'Waiting for 5 seconds...'
    time.sleep(5)
    print agent.dump()


main()
