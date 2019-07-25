import hasher

#Test output against known output
def test_readOption(capfd):
	hasher.readOption("unittests/HasherScan6-22-2019.csv", "all", "all")
	captured = capfd.readouterr()
	#print("OUT: {}".format(captured.out))
	assert captured.out == """Filename:test.csv\nFiletype:text/plain\nFilepath:../testing/test.csv\nHashtype:MD5-936107381FB4465444FDA46C8354E712\nSHAtype:SHA256-D7082E7AA5180764FE6C40CC82669C98DF65D62F0A7EBA4306F7A4560D4A7778\nsize:37\n----------\n"""

#Make sure error catching works
def test_errors(capfd):
	hasher.readOption("NonexistentFile.csv", "all", "all")
	captured = capfd.readouterr()
	assert captured.out == """NonexistentFile.csv is not a file.\n"""

#Test a hashlist with 1 hash
def test_readhashlist(capfd):
	hasher.readOption("unittests/HasherScan6-22-2019.csv", "all", "unittests/hashlist.txt")
	captured = capfd.readouterr()
	#print("OUT: {}".format(captured.out))
	assert captured.out == """Filename:test.csv\nFiletype:text/plain\nFilepath:../testing/test.csv\nHashtype:MD5-936107381FB4465444FDA46C8354E712\nSHAtype:SHA256-D7082E7AA5180764FE6C40CC82669C98DF65D62F0A7EBA4306F7A4560D4A7778\nsize:37\n----------\n"""

#Test our list that has more than 1 hash
#We get the same output twice, so might wanna fix that in future versions
def test_readhashlist2(capfd):
	hasher.readOption("unittests/HasherScan6-22-2019.csv", "all", "unittests/hashlist2.txt")
	captured = capfd.readouterr()
	#print("OUT: {}".format(captured.out))
	assert captured.out == """Filename:test.csv\nFiletype:text/plain\nFilepath:../testing/test.csv\nHashtype:MD5-936107381FB4465444FDA46C8354E712\nSHAtype:SHA256-D7082E7AA5180764FE6C40CC82669C98DF65D62F0A7EBA4306F7A4560D4A7778\nsize:37\n----------\nFilename:test.csv\nFiletype:text/plain\nFilepath:../testing/test.csv\nHashtype:MD5-936107381FB4465444FDA46C8354E712\nSHAtype:SHA256-D7082E7AA5180764FE6C40CC82669C98DF65D62F0A7EBA4306F7A4560D4A7778\nsize:37\n----------\n"""



