# hasher 2.0.0
hasher.py is a python script used for mobile device acquisition triage. 
It lists all files with their simple name, size, sha256 and md5 hashes.
It also lists the file path and file type for applicable files.

### Installation

#### Linux
 - `git clone https://github.com/IronCityCoder/hasher.git`
 - Move folder to desired directory

#### Windows
- Download ZIP
- Unpack in directory you want to run

### Running
`hasher.py path [-r] [-o {csv,txt}] [--type {file type}] [--hash {md5 or sha}]`

- **Path** is the file path for either scanning a directory or reading a previous report.
- **r** is a switch for reading from the path.
- **o** is a switch for scanning the path. You can choose the output type (csv or txt).
- **--type** for added filtering, you can only read or scan a certain file type (png, txt, etc).
- **--hash** like type, you can filter a specific hash when searching a report or directory.
