#!/usr/bin/python

import os
import sys
import time
import json
import helper

# ----------------------public settings:
# * the target device name, e.g., 'emulator:5555', None to automatically detect
target_device=None

# execute adb command specific to the target phone
def _adb(list, mute=True):
	return _cmd(["adb","-s",target_device]+list, mute)

# dump the info about an apk
def aapt_dump(apk):
	(ret,output) = _cmd(["aapt",'dump','badging',filepath], 0)
	_die(ret, "Failed to retrieve info of "+filepath)
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
	_die(pkg is None, 'Abnormal pkg:'+filepath+'\n'+output)
	return (pkg, mainact)

# ----------------------APIs:
# launch an installed app with short name
def adb_iaunch_app(pkg, mainact)
	if mainact is None:
		global _warning
		print 'Warning: no main activity to launch'
		_warning = True
		return 1
	launcher=pkg+"/"+mainact
	(ret, output) = _adb(["shell","am","start","-W",launcher],0)
	# parse the output to get exec time
	for line in output.splitlines():
		if line.startswith('TotalTime: '):
			exectime = int(line[line.find(' '):])
			_launch_log.append(exectime)
			break
	return 0

# install an app with a given short name
def adb_install_app(apk):
	(ret, output) = _adb(["install",apk], False)
	if ret:
		print 'Warning: failed to install', filepath
		print output
		global _warning
		_warning = True
	else:
		global _appdb
		print "Install", shortname, filepath
		_appdb[shortname]=_get_apkinfo(realpath)

# uninstall an app with a short name
def adb_uninstall_app(shortname):
	global _appdb
	if shortname not in _appdb:
		print 'Warning: failed to uninstall', shortname
		print 'Unknown short name'
		_warning = True
	else:
		(pkg, mainact) = _appdb[shortname]
		(ret, output) = _adb(['shell','pm','uninstall',pkg])
		if ret:
			print 'Warning: failed to uninstall', shortname
			print output
			_warning = True
		else:
			print "Uninstall", shortname
			del _appdb[shortname]

def check_adk():
	assert _cmd(["aapt","version"])[0] == 0,"aapt not found!"
	assert _cmd(["adb","version"])[0] == 0,"adb not found!"

def adb_find_device(name=None,nr=-1,ask_for_nr=True):
	(_, output) = _cmd(['adb','devices'], False)

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
		for device in device_list:
			print i,":",device
			i = i + 1
		while selected >= len(device_list):
			try:
				selected = input('Choose a target device: ')
			except KetyboardInterrupt:
				sys.exit(1)
		target_device = device_list[selected]	
	return target_device
