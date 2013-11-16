import subprocess
import os
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# helper: execute a raw command and selectively mute stdout and stderr
def _cmd(cmdlist, mute=1):
	if mute:
		fnull = open(os.devnull, "w")
		proc = subprocess.Popen(cmdlist, stdout = fnull, stderr = fnull)
		proc.communicate()
		fnull.close()
		return (proc.returncode, None)
	else:
		proc = subprocess.Popen(cmdlist, stdout = subprocess.PIPE, 
				stderr = subprocess.PIPE)
		(output, erroutput) = proc.communicate()
		return (proc.returncode, erroutput + output)
	
class MonkeyHelper:
	# call the aapt tool with arbitrary commands
	@staticmethod
	def aapt(cmdlist, mute = True):
		return _cmd(["aapt"] + cmdlist, mute)
	
	# retrieve the package name and main activity name of an apk
	@staticmethod
	def aapt_dump(apk):
		(ret, output) = MonkeyHelper.aapt(['dump','badging',apk], False)
		assert ret == 0, "Failed to retrieve the info of " + apk
		pkg = mainact = None
		for line in output.splitlines():
			if line.startswith('package:'):
				# get the package name
				(_, _, line) = line.partition("name='")
				pkg = line[:line.index("\'")]
			if line.startswith('launchable-activity:'):
				# get the main activity
				(_, _, line) = line.partition("name='")
				mainact = line[:line.index("\'")]
		assert pkg is not None, 'Abnormal pkg:'+apk+'\n'+output
		return (pkg, mainact)

# enhanced MonkeyDevice
class EMonkeyDevice:
	DOWN_AND_UP = MonkeyDevice.DOWN_AND_UP
	DOWN = MonkeyDevice.DOWN
	UP = MonkeyDevice.UP
	def __init__(self):
		self.dev = MonkeyRunner.waitForConnection()
	def broadcastIntent(self, uri, action, data, mimetype, extras, component, flags):
		self.dev.broadcastIntent(uri, action, data, mimetype, extras, component, flags)
	def drag(self, start, end, duration, steps):
		return self.dev.drag(start, end, duration, steps)
	def getProperty(self, key):
		return self.dev.getProperty(key)
	def getSystemProperty(self, key):
		return self.dev.getSystemProperty(key)
	def installPackage(self, path):
		self.dev.installPackage(path)
	def instrument(self, className, args):
		return self.dev.instrument(className, args)
	def press(self, name, t):
		self.dev.press(name, t)
	def reboot(self, into):
		self.dev.reboot(into)
	def removePackage(self, package):
		self.dev.removePackage(package)
	def shell(self, cmd):
		return self.dev.shell(cmd)
	def startActivity(self, uri, action, data, mimetype, extras, component, flags):
		self.dev.startActivity(uri, action, data, mimetype, extras, component, flags)
	def takeSnapshot(self):
		return self.dev.takeSnapshot()
	def touch(self, x, y, t):
		self.dev.touch(x, y, t)
	def type(self, message):
		self.dev.type(message)
	def wake(self):
		self.dev.wake()
