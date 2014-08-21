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
#   Ran Shu
#

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage


class SnapshortAgent :
    def __init__(self):
        self.device = MonkeyRunner.waitForConnection()
        
    def takeSnapShot(self):
        page=self.device.takeSnapshot()
        return page
    
    def saveSnapShot(self, page):
        fileName = raw_input('Enter a file name: ')
        page.writeToFile(fileName+'.png','png')
    
    def checkCurrentPage(self, pageCheck):
        currentPage=SnapshortAgent.takeSnapShot()
        SnapshortAgent.checkTwoPages(currentPage, pageCheck)
        
    def checkTwoPages (self, page1, page2):
        if page1.sameAs(page2, 1):
            return True
        else :
            return False
        
    def getSubPage (self, page):
        subPageSize = raw_input('Enter the x,y coordinates followed by the width and the height of the subImage: ')
        subPage=page.getSubImage(tuple(map(int,subPageSize.split(','))))
        return subPage
