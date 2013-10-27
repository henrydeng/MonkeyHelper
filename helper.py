import subprocess

# ----------------------helper functions:
# execute a raw command and mute all outputs
def _cmd(list, mute=1):
	if mute:
		proc = subprocess.Popen(list, stdout = _fnull, stderr = _fnull)
		proc.communicate()
		return (proc.returncode, None)
	else:
		proc = subprocess.Popen(list, stdout = subprocess.PIPE, 
				stderr = subprocess.PIPE)
		(output, erroutput) = proc.communicate()
		return (proc.returncode, erroutput + output)
