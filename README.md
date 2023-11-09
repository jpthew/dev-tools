# WhitelistRanger
WhitelistRanger is a tool that creates a list of IPs from whitelist and blacklist files, creating a clean target list. It handles CIDR notation in the input files. It can (SOON) also verify that a whitelist file does not include IPs from a chosen blacklist file.

## Features
1. Create a clean target list from whitelist and blacklist files.
2. Handles CIDR notation in the input files.
3. Verify that a whitelist file does not include IPs from a chosen blacklist file.
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



# Cewlest.py
Cewlest.py is a Python script that serves as a wrapper for gospider and a multithreaded adaptation of CeWL to spider and scrape URLs from a list of domains. It allows for clean output to stdout with -q/--quiet and output to file with -o/--output.

## Features
1. Multithreading: The most significant difference is that Cewlest.py uses multithreading to run CeWL. This means that it can process multiple URLs simultaneously, which can significantly speed up the web crawling process. In contrast, the standard CeWL processes URLs one at a time.

2. Integration with gospider: Cewlest.py integrates with gospider, a fast web spider written in Go. This allows Cewlest.py to leverage gospider's high-speed and efficient web crawling capabilities. gospider is known for its ability to fetch links from JavaScript, CSS, and HTML files and to handle cookies and sessions, which can help to uncover more URLs for CeWL to process.

3. Output Control: Cewlest.py provides options for controlling the output. It can output to stdout with -q/--quiet and output to a file with -o/--output. This gives users more flexibility in how they want to handle the output.


### Usage
```bash
python3 cewlest.py -i domains.txt -o output.txt -t 5
```
### Flags
```
-i, --input FILE: Input file of domains to spider and cewl. This argument is required.
-o, --output FILE: Output to file instead of stdout.
-v, --verbose: Verbose output.
-t, --threads <int>: Number of threads to use with cewl. Default is 5.
-q, --quiet: Disable all output except CeWL output. Ideal for piping STDOUT.
--gospider-output: Save gospider output to a file.
```

### Note
If both verbose and quiet modes are enabled, the script will exit with an error message.