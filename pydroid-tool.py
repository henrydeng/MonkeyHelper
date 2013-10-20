#!/usr/bin/python

import os
import sys
import subprocess
import time
import json

# ----------------------public settings:
install_path_prefix=''
result_folder='./'
# * the target device name, e.g., 'emulator:5555', None to automatically detect
target_device=None

# ----------------------private:
_fnull=open(os.devnull, "w")
_launch_log=[]
_appdb={}
_warning=False

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

# execute adb command specific to the target phone
def _adb(list, mute=1):
	return _cmd(["adb","-s",target_device]+list, mute)

def _die(cond, msg):
	if cond:
		print msg
		sys.exit(1)

def _get_apkinfo(filepath):
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
def launch_app(shortname):
	global _launch_log
	print "Launching", shortname
	_die(shortname not in _appdb, "Error: no " + shortname + " for launching")
	(pkg, mainact) = _appdb[shortname]
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

# wait for a while
def stall(seconds):
	print "Stall for",seconds,"seconds"
	time.sleep(seconds)

# install an app with a given short name
def install_app(shortname, filepath):
	realpath = install_path_prefix + filepath
	(ret, output) = _adb(["install",realpath], 0)
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
def uninstall_app(shortname):
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

# do the preparation, see detailed procedures in the function body
def prepare(load_db=1):
	# ads :-)
	print "Onebatch 1.0: automate installing and launching apps on Android phones"

	# test tool chain
	# TODO also check version maybe
	_die(_cmd(["aapt","version"])[0],"aapt not found in PATH!")
	_die(_cmd(["adb","version"])[0],"adb not found in PATH!")

	global target_device
	# detect target device(s)
	if target_device is None:
		(_, output) = _cmd(['adb','devices'], 0)

		# parse output to get a list of devices
		(_, _, output) = output.partition('List of devices attached')
		output = output.lstrip().rstrip()
		device_list = [line.partition('\t')[0] for line in output.splitlines()] 

		# ask the user to select if more than one devices
		if len(device_list) == 1:
			target_device = device_list[0]
		else:
			i = 0
			selected = len(device_list) + 1
			for device in device_list:
				print i,":",device
				i = i + 1
			while selected >= len(device_list):
				try:
					selected = input('Choose a target device: ')
				except KetyboardInterrupt:
					sys.exit(1)
			target_device = device_list[selected]	
	print "Device:",target_device

	if load_db:
		global _appdb
		dbfile = open('app_db.txt', 'r')
		_appdb = json.loads(dbfile.read())
		dbfile.close();

# if there are warnings stop the script
def check_warning():
	# check if warnings lead to errors
	_die(_warning, "Treat warnings as errors")

# start the monitor before launching things 
def start():
	# clear old logcat log
	_die(_adb(["shell","logcat","-c"])[0], "Failed to clear log!")

	# prepared
	print "--------------------------------------"

# clear the db
def clear_db():
	global _appdb
	_appdb={}

# finish the experiment
def finish():
	return 0 

# dump the results
def dump(save_db=1):
	print "--------------------------------------"
	# save the database if necessary
	if save_db:
		dbfile = open('app_db.txt', 'w')
		dbfile.write(json.dumps(_appdb))
		dbfile.close()
	print "Done=>", result_folder
