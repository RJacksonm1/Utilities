#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

if len(sys.argv) < 3:
	print 'Please specify a folder or VTF file as argument.'
	sys.exit(1)
try:
	version = int(sys.argv[1])
except:
	print 'Error: First argument must be a version number (only the "x" in "7.x")'
	sys.exit(1)
def vtf(vtf):
	global version
	f = open(vtf, 'rb')
	header = f.read(1024)
	if len(header) < 8:
		print 'Warning: Invalid VTF file:', vtf, '; skipping.'
		return
	if ord(header[8]) == version:
		print 'Warning:', vtf, 'is already version', version, '; skipping.'
		return
	print 'Converting', vtf
	header = header[:8] + chr(version) + header[9:]
	f2 = open(vtf + '.vtftmp', 'wb')
	while header:
		f2.write(header)
		header = f.read(1024)
	f.close()
	f2.close()
	os.remove(vtf)
	os.rename(vtf+'.vtftmp', vtf)

def passthrough(f):
	if not os.path.exists(f):
		print 'Warning:', f, 'doesn\'t exist; skipping.'
	elif os.path.isdir(f):
		if f[-1] != os.sep:
			f += os.sep
		for i in os.listdir(f):
			passthrough(f + i)
	elif os.path.isfile(f) and len(f) > 4:
		if f[-4:].lower() == '.vtf':
			vtf(f)

for f in sys.argv[2:]:
	passthrough(f)
print 'All done.'