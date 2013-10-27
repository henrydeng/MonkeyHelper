import helper

# the target device name, e.g., 'emulator:5555', None to automatically detect
target_device = None

def adb(cmdlist, mute=True):
	if target_device == None:
		return helper._cmd(["adb"]+cmdlist, mute)
	else:
		return helper._cmd(["adb","-s",target_device]+cmdlist, mute)

def aapt(cmdlist, mute=True):
	return helper._cmd(["aapt"]+cmdlist, mute)

# dump the info of an apk
def aapt_dump(apk):
	(ret,output) = aapt(['dump','badging',apk], False)
	assert ret == 0, "Failed to retrieve the info of "+apk
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

def adb_launch_app(pkg, mainact):
	if mainact is None: return None 
	launcher = pkg + "/" + mainact
	(_, output) = adb(["shell", "am", "start", "-W", launcher], False)
	return output

def adb_install_app(apk):
	(ret, output) = adb(["install", apk], False)
	if ret: return None
	else: return output

def adb_uninstall_app(pkg):
	(ret, output) = adb(['shell', 'pm', 'uninstall', pkg])
	if ret: return None
	else: return output

def check_adk():
	assert helper._cmd(["aapt","version"])[0] == 0,"aapt not found!"
	assert helper._cmd(["adb","version"])[0] == 0,"adb not found!"

def adb_find_device(name=None,ask_for_nr=True):
	(_, output) = helper._cmd(['adb','devices'], False)

	# parse output to get a list of devices
	(_, _, output) = output.partition('List of devices attached')
	output = output.lstrip().rstrip()
	devlist = [l.partition('\t')[0] for l in output.splitlines()] 

	# ask the user to select if more than one devices
	if len(devlist) == 1: return True
	global target_device
	if name is not None and name in devlist:
		target_device = name
		return True
	
	i = 0
	for device in devlist:
		print i,":",device
		i = i + 1
	selected = len(devlist) + 1
	while selected >= len(devlist):
		selected = input('Choose a target device: ')
	target_device = devlist[selected]	
	return target_device
