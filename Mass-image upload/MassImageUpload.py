import os, sys, wikiUpload, subprocess, hashlib

from Config import *

if len(sys.argv) < 2:
	print 'Please specify a folder or png as argument.'
	sys.exit(1)
	
def convertToFileName(f):
	onlyFileName = config["filename_prefix"] + f[f.rfind("\\")+1:] + config["filename_suffix"]
	return onlyFileName
		
uploader = wikiUpload.wikiUploader(config["user"], config["pass"], config["upload_url"])
failedItems = list()
successItems = list()

def upload(f):
	global uploader
	global failedItems
	global successItems
	
	try:
		if convertToFileName(f) != None:
			fileName = convertToFileName(f)
			print "Uploading: " + fileName
			try:
				uploader.upload(f, fileName, config["upload_summary"], '', overwrite=True)
				print "Done."
				successItems.append(fileName)
			except: 
				print "Upload failed."
				failedItems.append(fileName)
	except:
		print f + "... not found"
	
def passthrough(f):
	if not os.path.exists(f):
		print 'Warning:', f, 'doesn\'t exist; skipping.'
	elif os.path.isdir(f):
		if f[-1] != os.sep:
			f += os.sep
		for i in os.listdir(f):
			passthrough(f + i)
	elif os.path.isfile(f) and len(f) > 4:
		if f[-4:].lower() == '.png':
			upload(f)

for f in sys.argv[1:]:
	passthrough(f)
print "All done."

for winners in successItems:
	print winners + "... UPLOADED"
	
if len(failedItems) != 0:
	for losers in failedItems:
		print losers + "... FAILED"
	
	print `len(failedItems)`
	if (raw_input("Enter \"Y\" to re-try uploading the failed items.\n").upper() == "Y"):
		for losers in failedItems:
			upload(losers)
		
			