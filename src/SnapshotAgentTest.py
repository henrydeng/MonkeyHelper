from SnapshotAgent import SnapshotAgent


def main():
    print "working"
<<<<<<< HEAD:src/SnapshortAgentTest.py
    tools = SnapshortAgent()
=======
    tools=SnapshotAgent()
>>>>>>> 9aed59fd8b5cd2aeda8ad502056ddf7a3e23575e:src/SnapshotAgentTest.py
    print "working 2"
    savedImage = tools.takeSnapshot()
    tools.saveSnapshot(savedImage, 'tempPic')
    print "working 3"
    print tools.compareSnapshots(savedImage, savedImage)
    print "working 4"
    print tools.compareSnapshots(savedImage, tools.loadSnapshot('screen_shot2.png'))
    print "working 5"
    print tools.takeAndCompareSnapshots(tools.loadSnapshot('screen_shot2.png'))
    print "working 6"
    savedImage2 = tools.getSubSnapshot(tools.loadSnapshot('screen_shot2.png'), (100, 100, 100, 100))
    tools.saveSnapshot(savedImage2, 'tempPic2')
    print "working 7"


if __name__ == "__main__":
    main()
