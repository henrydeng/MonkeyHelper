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
