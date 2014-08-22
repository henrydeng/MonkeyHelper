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
# Contributor(s):
#   Mingyuan Xia
#

class LogcatAgent:
    MAIN = 'main'
    EVENTS = 'events'
    RADIO = 'radio'
    """ LogcatAgent controls logcat, the logging facility of Android"""
    def __init__(self, device):
        """ Initialize the agent with a given device
        @param device: should be an EMonkeyDevice
        """
        self.device = device
    def logcat(self, args):
        """ Send a raw logcat command and return its output"""
        s = "logcat"
        for arg in args:
            s += ' ' + arg
        return self.device.shell(s).encode('utf-8')
    def clear(self):
        """ Clear the logcat logs"""
        self.logcat(['-c'])
    def dumpBuf(self, buf = MAIN):
        return self.logcat(['-b ', buf])
    def dump(self, fmt = None, filterTuples = []):
        """ Dump the logcat logs with given filters and formats
        @param fmt: the output format
        @param filterTuples: a list of (TAG,LEVEL) tuples that specify filtering 
        according to Android doc, LEVEL could be:
        V - Verbose (lowest priority)
        D - Debug
        I - Info
        W - Warning
        E - Error
        F - Fatal
        S - Silent (highest priority, on which nothing is ever printed)
        """
        cmd = ['-d']
        if fmt is not None:
            cmd.append('-v')
            cmd.append(fmt)
        for tp in filterTuples:
            cmd.append('%s:%s' % tp)
        return self.logcat(cmd)
