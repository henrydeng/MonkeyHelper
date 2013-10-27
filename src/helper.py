import subprocess
import os

_fnull = open(os.devnull, "w")

# ----------------------helper functions:
# execute a raw command and mute all outputs
def _cmd(cmdlist, mute=1):
	if mute:
		proc = subprocess.Popen(cmdlist, stdout = _fnull, stderr = _fnull)
		proc.communicate()
		return (proc.returncode, None)
	else:
		proc = subprocess.Popen(cmdlist, stdout = subprocess.PIPE, 
				stderr = subprocess.PIPE)
		(output, erroutput) = proc.communicate()
		return (proc.returncode, erroutput + output)
