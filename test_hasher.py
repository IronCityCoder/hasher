import hasher

def test_readOption(capfd):
	readOption("../testing/test.csv", "all", "all")
	captured = capfd.readouterr()
  #The documentation doesn't explain what out/err do so we need to test them ourselves.
	print(captured.out)
	#assert captured.out == ""

'''
Filename:test.csv
Filetype:text/plain
Filepath:../testing/test.csv
Hashtype:MD5-936107381FB4465444FDA46C8354E712
SHAtype:SHA256-D7082E7AA5180764FE6C40CC82669C98DF65D62F0A7EBA4306F7A4560D4A7778
size:37
----------
'''
