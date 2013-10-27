import helper

# ----------------------public settings:
# * the target device name, e.g., 'emulator:5555', None to automatically detect
target_device=None

# execute adb command specific to the target phone
def adb(cmdlist, mute=True):
	return helper._cmd(["adb","-s",target_device]+cmdlist, mute)

def aapt(cmdlist, mute=True):
	return helper._cmd(["aapt"]+cmdlist, mute)

# dump the info about an apk
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

# ----------------------APIs:
# launch an installed app with short name
def adb_launch_app(pkg, mainact):
	if mainact is None:
		global _warning
		print 'Warning: no main activity to launch'
		_warning = True
		return 1
	launcher=pkg+"/"+mainact
	(_, output) = adb(["shell","am","start","-W",launcher],0)
	# parse the output to get exec time
	for line in output.splitlines():
		if line.startswith('TotalTime: '):
			break
	return 0

# install an app with a given short name
def adb_install_app(apk):
	(ret, output) = adb(["install",apk], False)
	if ret:
		print 'Warning: failed to install', apk
		print output
		global _warning
		_warning = True

# uninstall an app with a short name
def adb_uninstall_app(pkg):
	global _appdb
	(ret, output) = adb(['shell','pm','uninstall',pkg])
	if ret:
		print output
		_warning = True

def check_adk():
	assert helper._cmd(["aapt","version"])[0] == 0,"aapt not found!"
	assert helper._cmd(["adb","version"])[0] == 0,"adb not found!"

def adb_find_device(name=None,nr=-1,ask_for_nr=True):
	(_, output) = helper._cmd(['adb','devices'], False)

	# parse output to get a list of devices
	(_, _, output) = output.partition('List of devices attached')
	output = output.lstrip().rstrip()
	devlist = [l.partition('\t')[0] for l in output.splitlines()] 

	# ask the user to select if more than one devices
	if len(devlist) == 1:
		target_device = devlist[0]
	else:
		i = 0
		selected = len(devlist) + 1
		for device in devlist:
			print i,":",device
			i = i + 1
		while selected >= len(devlist):
			selected = input('Choose a target device: ')
		target_device = devlist[selected]	
	return target_device
