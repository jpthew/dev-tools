# WhitelistRanger
WhitelistRanger is a tool that creates a list of IPs from whitelist and blacklist files, creating a clean target list. It handles CIDR notation in the input files. It can also verify that a whitelist file does not include IPs from a chosen blacklist file.

## Features
Create a clean target list from whitelist and blacklist files.
Handle CIDR notation in the input files.
Verify that a whitelist file does not include IPs from a chosen blacklist file.
### Usage
```bash 
python whitelistranger.py -w whitelist.txt -b blacklist.txt -o output.txt
```
### Flags
* -h: Help menu.
* -w: Whitelist file.
* -b: Blacklist file.
* -o: Output file.
* -v: Verbose (print to stdout).
## Example
```bash
python whitelistranger.py -w whitelist.txt -b blacklist.txt -o output.txt
```
This will create a new file called output.txt containing a list of all the IPs in the whitelist file that are not in the blacklist file.
