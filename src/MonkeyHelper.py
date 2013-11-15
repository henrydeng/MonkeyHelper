import subprocess
import os

# helper: execute a raw command and selectively mute stdout and stderr
def _cmd(cmdlist, mute=1):
	if mute:
		with open(os.devnull, "w") as fnull:
			proc = subprocess.Popen(cmdlist, stdout = fnull, stderr = fnull)
			proc.communicate()
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

