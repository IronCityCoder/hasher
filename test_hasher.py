import hasher

def test_readOption(capfd):
	hasher.readOption("HasherScan6-22-2019.csv", "all", "all")
	captured = capfd.readouterr()
  #The documentation doesn't explain what out/err do so we need to test them ourselves.
	print("OUT: {}".format(captured.out))
	assert captured.out == """Filename:test.csv\nFiletype:text/plain\nFilepath:../testing/test.csv\nHashtype:MD5-936107381FB4465444FDA46C8354E712\nSHAtype:SHA256-D7082E7AA5180764FE6C40CC82669C98DF65D62F0A7EBA4306F7A4560D4A7778\nsize:37\n----------\n"""

