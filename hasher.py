#!/usr/bin/env python3
# import all needed modules
import argparse
import os
import hashlib
from sys import argv
from datetime import datetime as dt
import pdb
import pathlib

# In case the computer does not have magic installed
try:
		import magic 

except ImportError:
		print("python-magic is not installed! \n\
			Install it with pip: \n\
			-  pip install python-magic \n\
			Or go to the Github page: \n\
			- https://github.com/ahupp/python-magic")

'''
hasher.py is a python script used for mobile device acquisition triage. 
It lists all files with their simple name, size, sha256 and md5 hashes.
It also lists the file path and file type for applicable files.

arg.py path [-h] [-r] [-o {csv,txt}] [--type TYPE] [--hash HASH] 

'''
#This function walks through the given directory.
def scanDir(directory, output, filetype='all', hashtype='all') :
	global ProcessCount
	global ErrorCount

	ProcessCount = 0
	ErrorCount = 0
	path = pathlib.Path(directory)
	files = path.rglob("*")
	date = "{}-{}-{}".format(dt.today().month, dt.today().day, dt.today().year)
	m = magic.Magic(mime=True)
	with open("HasherScan{}.{}".format(date, output), "w+") as ofile:
		for file in files:
			if file.is_file():
				#Check file type and hashes.
				ftype = m.from_file(filePath)
				with open(filePath, 'rb') as fp:
					fdata = fp.read()
				hash = hashlib.md5 ()
				hash256 = hashlib.sha256 ()
				hash.update(fData)
				hash256.update(fData)
				hexMD5 = hash.hexdigest().upper()
				hexSHA = hash256.hexdigest ().upper()
				#If a filetype is entered we check it.
				run = False
				if filetype != 'all' and hashtype != 'all':
					if filetype in ftype and hashtype == hexMD5 or hashtype == hexSHA:
						run = True
						
				elif hashtype != 'all':
					if hashtype == hexMD5 or hashtype == hexSHA:
						run = True

				elif filetype != 'all':
					if filetype in ftype:
						run = True		

				if run:
					runThrough(str(file), file, ftype, hexMD5, hexSHA, ofile)
		
#where to handle hash logic 
def runThrough(filePath, pathObj, filetype, md5, sha, ofile):
	
	#Grab the information for each file in a directory.	
	theFileStats = os.stat(filePath)
	(mode, ino, dev, nlink, uid, gid, size, altime, mtime, ctime,) = os.stat(filePath)
						
	hHFile = {
		'hashType': 'MD5',
		'SHAtype': 'SHA256',
		'hexMD5': md5,
		'hexSHA': sha,
		'size': size,
		'FileName': pathObj.name,
		'FilePath': filePath,
		'FileType': filetype
	}

	form = 'Filename: {FileName},Filetype: {FileType},\
	Filepath: {FilePath}, Hashtype: {hashType} - {hexMD5},\
	SHAtype: {SHAtype} - {hexSHA}, size: {size}\n'.format(**hHFile).replace('    ','')		
	ofile.write(form)
                         

def readFile(filePath, fileType = 'all' hashType = 'all')
	with open(filePath, "rb") as fp:
		#All our store is stored as csv anyways so separate on commas
		for line in fp:
			newLine = line.split(",")
			if fileType == 'all' and hashType == 'all':
				printer(newLine)
			elif fileType != 'all' and hashType != 'all':
				if fileType in newLine and hashType in newLine:
					printer(newLine)
			elif fileType != 'all':
				if fileType in newLine:
					printer(newLine)
			elif hashType != 'all':
				if hashType in newLine:
					printer(newLine)
					
def printer(linearr):
	for i in linearr:
		print(i)
		print("-" * 10)

#We will likely need some error messages during testing.		
def callError():
	pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Hasher 2.0 is a file stat program for mobile devices.')
	group = parser.add_mutually_exclusive_group(required=True)
	parser.add_argument('path', help="Path: The path files will be read or scanned from.")
	group.add_argument('-r', action= "store_true", help="Read: Instead of scanning a folder it will read a folder.")
	group.add_argument('-o', choices=["csv", "txt"], help="Output: Determines the type of output of the scan.")
	parser.add_argument('--type', default = "all", help="Type: Will only scan files of a certain type.")
	parser.add_argument('--hash', default = "all", help="Hash: Takes in a file that stores a list of hashes and scans matching files.")
	#https://github.com/mac4n6/APOLLO/blob/master/apollo.py
	#https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
	args = parser.parse_args()

	global path
	path = args.path

	#Because r and o are in a group, they have to pick one.
	if args.r:
		print("READING")
		readFile(path, args.type, args.hash)
	#Scan
	elif args.o:
		print("SCANNING")
		scanDir(path, args.o, args.type, args.hash)
