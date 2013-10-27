#!/usr/bin/python
import pyadk 

pyadk.check_adk()
pyadk.adb_find_device()

pyadk.adb_install_app("1.apk")

pyadk.adb_launch_app("test")
