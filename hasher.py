#!/usr/bin/env python3

import argparse
import pathlib
import hashlib
import zlib
from sys import argv
from datetime import datetime as dt

try:
		import magic 

except ImportError:
		print("python-magic is not installed! \n\
			Install it with pip: \n\
			-  pip install python-magic \n\
			Or go to the Github page: \n\
			- https://github.com/ahupp/python-magic")

# TODO Build new Unit-tests for 2.0.2 that check the filters
# TODO Push 2.0.2 once unit-testing passes
# TODO test for .lower() in filter_args

# Opens a file and appends stored values to a list.
def open_filter_file(file_name):
	stack = []
	with open(file_name, "r") as file:
		if file_name[-3:] == "csv":
			# Split by CSV
			lines = (line.split(",") for line in file)
			# Remove empty lines
			lines = (line for line in lines if line)
		else:
			# Split by new line 
			lines = (line.rstrip() for line in file)
			lines = (line for line in lines if line)

		for line in lines:
			stack.append(line)

	return stack

# Determine if a file type is provided for parsing hash or filetype filters.
# Returns a list of either "all" or specific hashes/file types to search for.
def filter_args(filter_type):
	stack = [filter_type]
	acceptable_extensions = [".txt", ".csv"]

	# Determine if filter_type ends with .txt or .csv
	if any(x in filter_type for x in acceptable_extensions ):
		try:
			# Wipe stack memory and replace it.
			stack.clear()
			stack = open_filter_file(filter_type)
		except:
			# Use callError to print to error log.
			call_error("Error reading a filter file.")			
	return stack

# Formats the output of reports.
def report_formatter(output):
	date = dt.today()
	file = f"{date.day}-{date.month}-{date.year}"
	return f"Scan{file}.{output}"

# Gets the hashes of a file.
# Block size is set to 1024 bits by default. 
def hashing(file, block_size = 2**10):
	func = f"hashlib.{FORMAT_HASH}()"
	# Build the right object based on our global format_hash
	file_hash = eval(func)
	with open(str(file), "rb") as read_file:
		# Builds the hash in chunks to read large files.
		# Keeping the error handling for safety.
		try:
			while True:
				buffer = read_file.read(block_size)
				if not buffer:
					break
				file_hash.update(buffer)

			file_hash = file_hash.hexdigest()
			# Depending on casing preference, return lower or uppercase.
			return file_hash.upper() if HASH_CASE else file_hash
		except:
			call_error(f"{str(file)} is too large! Size: {file.stat().st_size}")

# Determine if a filter we want is in the file.
def logic_tree(stack, info):
	for count, value in enumerate(stack):
		if value.lower().rstrip() in info:
			return True

# Checks combinations of booleans
def combinations(all_hashes, all_files, type_bool, hash_bool):
	if not(all_hashes and all_files):
		if not(hash_bool and type_bool):
			return False
	elif not(all_hashes and hash_bool):
		return False
	elif not(all_files and type_bool):
		return False	
	return True
		
# Walks through the directory and collects info about each file.
def scan_dir(directory, file_type = "all", hash_type = "all"):
	path = pathlib.Path(directory)
	# Narrow files scanned
	if file_type == "all":
		files = path.rglob("*")
	else:
		files = path.rglob(f"*.{file_type}")
	#files = [file for file in files if file.is_file()]
	file_name = report_formatter("csv")
	
	# Set up the mls -lls sagic-byte object for determing file type
	m = magic.Magic(mime=True) # Set mime to False for different output
	
	with open(file_name, "w+") as output_file:
		for file in files:
			try:
				if file.is_file():
					item_type = m.from_file(str(file))
					file_hash = hashing(file)
					# List of what the user wants to filer.
					# If nothing is supplied, should be "all".
					filter_hashes = filter_args(hash_type)
					filter_extensions = filter_args(file_type)
					
					# Booleans to determine what we scan
					all_hashes, all_files = filter_hashes[0] == "all", filter_extensions[0] == "all"
					
					hash_bool = True if all_hashes else logic_tree(filter_hashes, file_hash)
					type_bool = True if all_files else logic_tree(filter_extensions, item_type)
					# Check combinations of booleans
					if combinations(all_hashes, all_files, type_bool, hash_bool):

						# We either have the types being "all" or they match filters
						# Clean up the args being passed
						file_stats = file.stat()
						
						# Modify output based on output_type
						output = f"Filename: {file.name}, Filetype: {item_type}, Filepath: {str(file)}, Hashtype: {FORMAT_HASH} - {file_hash}, size: {file_stats.st_size}\n".replace('    ','')
						output_file.write(output)
			except:
				call_error(f"{str(file)} throws a permission error!")

# Will go through a report and print out information.			
def read_report(path, file_type = "all", hash_type = "all"):
	global FORMAT_HASH
	global HASH_CASE
	FORMAT_HASH = "md5"
	HASH_CASE = "false"
	path = pathlib.Path(path)
	if path.is_file():
		# Setting up booleans for filtering.
		filter_hashes = filter_args(hash_type)
		#print(filter_hashes)
		filter_extensions = filter_args(file_type)
		all_hashes, all_files = filter_hashes[0] == "all", filter_extensions[0] == "all"
		results = open_filter_file(str(path))
		# Go over each line and check if it matches what we are looking for.
		for count, value in enumerate(results):
			# We need to re-hash the file being checked
			# Otherwise we would need to just store all the hash types
			# Will need to see which is more costly
			hash_bool = True if all_hashes else logic_tree(filter_hashes, value[3])
			type_bool = True if all_files else logic_tree(filter_extensions, value[1])
	
			file_hash = hashing(value[2].split(" ")[-1].rstrip())
			if combinations(all_hashes, all_files, type_bool, hash_bool):
				print_result(value, file_hash)
	else:
		call_error(f"{path} is not a file.")

# Formatting the printed output.
def print_result(results, file_hash):
	for count, value in enumerate(results):
		if count == 3:
			print(f"Hashtype: {FORMAT_HASH}-{file_hash}")
		else:
			print(value.rstrip().replace(' ', ''))
		if count == len(results) - 1:
			print("-" * 10)
				

#We will likely need some error messages during testing.		
def call_error(message):
	print(f"Error occured: {message}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Hasher 2.0.2 is a file stat program for mobile devices.')
	group = parser.add_mutually_exclusive_group(required=True)
	parser.add_argument('path', help="Path: The path files will be read or scanned from.")
	group.add_argument('-r', action= "store_true", help="Read: Instead of scanning a folder it will read a folder.")
	group.add_argument('-o', choices=["csv"], help="Output: Determines the type of output of the scan.")
	parser.add_argument('--type', default = "all", help="Type: Will only scan files of a certain type.")
	parser.add_argument('--hash', default = "all", help="Hash: Takes in a file that stores a list of hashes and scans matching files.")
	parser.add_argument('-f', choices=["md5", "sha1", "sha256"], default = "md5", help = "Format: Type of hash that will be stored or printed,")
	parser.add_argument('-u', action='store_true', help = "Uppercase hash format.")
	args = parser.parse_args()

	global FORMAT_HASH
	FORMAT_HASH = args.f

	global HASH_CASE
	HASH_CASE = args.u

	#Because r and o are in a group, they have to pick one.
	if args.r:
		read_report(args.path, args.type, str(args.hash))
	#Scan
	elif args.o:
		scan_dir(args.path, args.type, str(args.hash))
