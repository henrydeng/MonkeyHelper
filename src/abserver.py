import urllib
import json
import sys
from MonkeyHelper import MonkeyHelper

def get_file_path(dbentry, fname):
	"""get the file path belonging to the db entry"""
	return ""

def write_file_once(dbentry, fname, data):
	# f = open(get_file_path(dbentry, fname), 'w')
	f = sys.stdout
	print "writing fname: " + fname
	f.write(data)
	f.close()

def download_apk(url, apkpath):
	urllib.urlretrieve(url, apkpath)
	

def create_dbentry(apk):
	dbentry = {}
	# fetch the apk
	apk = get_file_path(dbentry, "apk.apk")
	dbentry["apk"] = True 

	# get the jar

	# get basic info
	info = MonkeyHelper.aapt_dump(apk)
	dbentry.update(info)

	# write the db in case the tool chain is broken
	write_file_once(dbentry, "entry", json.dumps(dbentry))

	# launch the tool chain

	# update the db
	write_file_once(dbentry, "entry", json.dumps(dbentry))


