# hasher
[![version](https://img.shields.io/badge/Version-2.0.1-blue.svg)](https://github.com/IronCityCoder/hasher)
[![stability](https://img.shields.io/badge/stability-experimental-orange.svg)](https://github.com/IronCityCoder/hasher)

hasher.py is a python script used for mobile device acquisition triage. 
It lists all files with their simple name, size, sha256 and md5 hashes.
It also lists the file path and file type for applicable files.

### 2.0.1 updates include:
- Able to pass in a .txt or .csv new-line separated list to the --hash flag

## Todo

- Update --hash to handle comma separated values as well as new line
- Store X most recent reports 
- Add unit testing for main scanning
- Put hash filtering and file filtering in their own functions
 

### Installation

#### Linux
- Open up command line.
 - `git clone https://github.com/IronCityCoder/hasher.git`
 - Move folder to desired directory with `mv` command.
- `pip3 install pathlib`

#### Windows
- Download ZIP
- Unpack in directory you want to run
- `pip3 install pathlib`

### Running
`./hasher.py path [-r] [-o {csv,txt}] [--type {file type}] [--hash {md5 or sha}]`

- **Path** is the file path for either scanning a directory or reading a previous report.
- **r** is a switch for reading from the path.
- **o** is a switch for scanning the path. You can choose the output type (csv or txt).
- **--type** for added filtering, you can only read or scan a certain file type (png, txt, etc).
- **--hash** like type, you can filter a specific hash when searching a report or directory.

### Testing

Unit testing is done through pytest in the included `test_hasher.py` file. As of now unit testing is only used for reading out a report. I will start working on tests for scanning and expanding the current tests. An example .csv file has been uploaded to be used with the testing program. Move to the directory your code is in and run `py.test` and it will detect the testing file and run it. 
