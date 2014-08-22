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

""" LogcatAgent controls logcat, the logging facility of Android
"""
class LogcatAgent:
    def __init__(self, device):
        self.device = device
    def clear(self):
        self.device.shell('logcat -c')
    def dump(self, fmt = None, filterTuples = []):
        """
        @param fmt: the output format
        @param filterTuples: a list of (TAG,LEVEL) tuples that specifies the filter
        according to Android doc, LEVEL could be:
        V - Verbose (lowest priority)
        D - Debug
        I - Info
        W - Warning
        E - Error
        F - Fatal
        S - Silent (highest priority, on which nothing is ever printed)
        """
        cmd = 'logcat -d'
        if fmt is not None:
            cmd += ' -v ' + fmt
        for tp in filterTuples:
            cmd += ' %s:%s' % tp
        return self.device.shell(cmd).encode('utf-8')
