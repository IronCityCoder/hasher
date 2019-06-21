#!/usr/bin/env python3
# import all needed modules
import os
import hashlib
from sys import argv
import datetime
import pdb
import pathlib

# in case the computer does not have magic installed
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

Usage: ./hasher.py [Directory]

Examples:
./hasher.py directory
./hasher.py "directory"
./hasher.py directory/subdirectory 

Dependencies: 
pip install python-magic
'''

#This function walks through the given directory.
def processDirectories(directory) :


	global ProcessCount
	global ErrorCount

	ProcessCount = 0
	ErrorCount = 0
    
    path = pathlib.Path(directory)
    files = path.rglob("*")
    for file in files:
        result = hashFile(str(file), pathObj)
        if result:
            ProcessCount += 1
        else:
            ErrorCount += 1
    #fname = os.path.join(root, file)
    #result = hashFile(fname, file)

#Grab the information for each file in a directory.			
def hashFile(filePath, pathObj) :
    try:
        #Any errors will be processed in the exception clause   
        fp = open(filePath , 'rb')
        fData = fp.read()
        fp.close()
                                
        theFileStats = os.stat(filePath)
        (mode, ino, dev, nlink, uid, gid, size, altime, mtime, ctime,) = os.stat(filePath)

        hash = hashlib.md5 ()
        hash256 = hashlib.sha256 ()
        hash.update(fData)
        hash256.update(fData)
                               
        #Trying the magic library for cross-platform support
        m = magic.Magic(mime=True)
        ftype = m.from_file(filePath)

        hHFile = {
            'hashType': 'MD5',
            'SHAtype': 'SHA256',
            'hexMD5': hash.hexdigest().upper(),
            'hexSHA': hash256.hexdigest ().upper(),
            'size': size,
            'FileName': pathObj.name,
            'FilePath': filePath,
            'FileType': ftype
        }
                                
        # print the results
        #pdb.set_trace()                                                   
        print ('Filename: {FileName}, \n\
        Filetype: {FileType}, \n\
        Filepath: {FilePath}, \n\
        Hashtype: {hashType}, {hexMD5} \n\
        SHAtype: {SHAtype}, {hexSHA} \n\
        size: {size} \n\
        ----------'.format(**hHFile).replace('    ','') )
                                
        #Returning True since any error catches return false to iterate ErrorCount.
        return True  
        
    except IOError:
        #An exception occured when processing the file
        print (theFile + ' File Processing Error')
            return False
                
if __name__ == '__main__' :
        #Grab our arguments. 
        #Script is the name of our script
        #Directory is the name of the directory to start traversal.
        script, directory = argv
        processDirectories(directory)
