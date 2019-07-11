#!/usr/bin/env python3
# import all needed modules
import argparse
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
def scanDir(directory, output, fileType='all', hashType='all') :
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
				ftype = m.from_file(str(file))
				with open(str(file), 'rb') as fp:
					fData = fp.read()
				hash = hashlib.md5 ()
				hash256 = hashlib.sha256 ()
				hash.update(fData)
				hash256.update(fData)
				hexMD5 = hash.hexdigest().upper()
				hexSHA = hash256.hexdigest ().upper()
				#If a filetype is entered we check it.
				
				hashStack = [hashType]
				allHash = True
				acceptableTypes = [".txt", ".csv"]

				#We go through our hash list and put hashes in a list.
				if any(x in hashType for x in acceptableTypes):
					try:
						with open(hashType, "r") as hs:
							hashStack = []
							allHash = False
							#Strip out empty lines.
							lines = (line.rstrip() for line in hs)
							lines = (line for line in lines if line)
							for line in lines:
								hashStack.append(str(line))
					except:
						#Use callError to print to error log.
						print("Error reading hash file.")

				#Test out this new implementation.
				for i, v in enumerate(hashStack):
					filebool = fileType in ftype #i.e is png in ftype?
					hashbool = v in [hexMD5, hexSHA] #do hashes match?

					fbool = fileType != 'all' #file filtering on or off?

					if fbool and not allHash:
						if not (filebool and hashbool):
							continue
					elif fbool:
						if not filebool:
							continue
					elif not(allHash):
						if not hashbool:
							continue
					#If we pass filters we will format file info below.
					runThrough(str(file), file, ftype, hexMD5, hexSHA, ofile)
		
#where to handle hash logic 
def runThrough(filePath, pathObj, filetype, md5, sha, ofile):
	#Stats about the file are stored here in an object.
	#For future versions we can have flags to grab specific information.
	fileStats = pathObj.stat()
	
	#Grab the information for each file in a directory.						
	hHFile = {
		'hashType': 'MD5',
		'SHAtype': 'SHA256',
		'hexMD5': md5,
		'hexSHA': sha,
		'size': fileStats.st_size,
		'FileName': pathObj.name,
		'FilePath': filePath,
		'FileType': filetype
	}

	ofile.write('Filename: {FileName},Filetype: {FileType}, Filepath: {FilePath}, Hashtype: {hashType} - {hexMD5}, SHAtype: {SHAtype} - {hexSHA}, size: {size}\n'.format(**hHFile).replace('    ',''))

def readOption(filePath, fileType = "all", hashType = "all"):
	path = pathlib.Path(filePath)
	if path.is_file():
		with open(filePath, "r") as fp:
			try:
				#All our store is stored as csv anyways so separate on commas
				for line in fp:
					newLine = line.split(",")
					#Unlike in the scanning portion, we are working with a list now.
					#So we have to compare the indexes of a list with our filters.
					#Set up variables for easier logic.
					newType = newLine[1]
					hashStack = [hashType]
					allHash = True
					acceptableTypes = [".txt", ".csv"]
					if any(x in hashType for x in acceptableTypes):
						try:
							with open(hashType, "r") as hs:
								hashStack = []
								allHash = False
								#Strip out empty lines.
								lines = (line.rstrip() for line in hs)
								lines = (line for line in lines if line)
								for line in lines:
									hashStack.append(str(line))
						except:
							#Use callError to print to error log.
							print("Error reading hash file.")
					#We go over our list of hashes
					#and check that the filetype and hashes match up
					#if allHash is true, we don't even need to check hashes
				
					for i, v in enumerate(hashStack):
						check = v in newLine[3], newLine[4]
						if fileType != 'all' and not allHash:
							if not(fileType in newType and check):
								continue
						elif fileType != 'all':
							if not(fileType in newType):
								continue
						elif not allHash:
							if not check:
								continue
						printer(newLine)
			except:
				#Print errors out when reading in data.
				print("Error reading the file: {}".format(filePath))
	else:
		print("{} is not a file.".format(filePath))

def printer(linearr):
	for i, v in enumerate(linearr):
		print(v.rstrip().replace(' ', ''))
		if i == len(linearr) - 1:		
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
		readOption(path, args.type, str(args.hash))
	#Scan
	elif args.o:
		scanDir(path, args.o, args.type, str(args.hash))
