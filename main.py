#!/usr/bin/python
import urllib
import json
import sys

# get the file path belonging to the db entry
def get_file_path(dbentry, fname):

def write_file_once(dbentry, fname, data):
	# f = open(get_file_path(dbentry, fname), 'w')
	f = sys.stdout
	print "writing fname: " + fname
	f.write(data)
	f.close()

def main(url):
	# fetch the apk
	apk = get_file_path(dbentry, "apk.apk")
	urllib.urlretrieve(url, apk)
	dbentry["apk"] = True 

	# get the jar

	# get basic info
	info = pyadk.aapt_dump(apk)
	dbentry.update(info)

	# write the db in case the tool chain is broken
	write_file_once(dbentry, "entry", json.dumps(dbentry))

	# launch the tool chain

	# update the db
	write_file_once(dbentry, "entry", json.dumps(dbentry))

def prepare():
	pyadk.check_adk()
	pyadk.adb_find_device()

