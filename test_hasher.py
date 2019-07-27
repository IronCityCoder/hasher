import hasher
#Test output against known output
def test_readOption(capfd):
	hasher.read_report("Scan26-7-2019.csv", "all", "all")
	captured = capfd.readouterr()
	#print("OUT: {}".format(captured.out))
	assert captured.out == """Filename:test2.csv\nFiletype:text/plain\nFilepath:unittests/test1/test2.csv\nHashtype: md5-D0E4643627CBD3B3DCBE6869D19842DC\nsize:24\n----------\nFilename:test.csv\nFiletype:text/plain\nFilepath:unittests/test1/test.csv\nHashtype: md5-A4F67810ED9271018F5A31CA3BCE2888\nsize:30\n----------\n"""

#Make sure error catching works
def test_errors(capfd):
	hasher.read_report("NonexistentFile.csv", "all", "all")
	captured = capfd.readouterr()
	assert captured.out == """Error occured: NonexistentFile.csv is not a file.\n"""

#Test a hashlist with 1 hash
def test_readhashlist(capfd):
	hasher.read_report("Scan26-7-2019.csv", "all", "unittests/hashlist.txt")
	captured = capfd.readouterr()
	#print("OUT: {}".format(captured.out))
	assert captured.out == """Filename:test.csv\nFiletype:text/plain\nFilepath:unittests/test1/test.csv\nHashtype: md5-A4F67810ED9271018F5A31CA3BCE2888\nsize:30\n----------\n"""




