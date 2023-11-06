#!/usr/bin/python3

# NEED TO CONVERT TO ARGPARSE #
import sys
import ipaddress

def read_file(filename):
    with open(filename, 'r') as f:
        ips = f.read().splitlines()
    ips_list = []
    for ip in ips:
        if "/" in ip:
            for ip in ipaddress.IPv4Network(ip, False):
                ips_list.append(str(ip))
        else:
            ips_list.append(ip)
    return ips_list

def remove_blacklisted_ips(whitelist, blacklist):
    for ip in blacklist:
        if ip in whitelist:
            whitelist.remove(ip)
    return whitelist

def print_help():
    print("\nThis tool creates a list of IPs from whitelist and blacklist files, creating a clean target list. It handles CIDR notation in the input files.\nIt can also verify that a whitelist file does not include IPs from a chosen blacklist file with --verify\n\nUsage: whitelistranger.py -w whitelist.txt -b blacklist.txt -o output.txt\n\n Flags:\n\n check: Use check mode to verify whitelist file. (whitelistranger.py check -h) for more information\n -h: This help menu\n -w: Whitelist file\n -b: Blacklist file\n -o: Output file\n -v: Verbose (print to stdout)\n")

def print_check_help():
    print("Check a whitelist file against a blacklist file to see if it contains any blacklisted IPs. It handles CIDR notation in the input files.\n\nUsage: whitelistranger.py check -w whitelist.txt -b blacklist.txt\n\n Flags:\n\n -h: This help menu\n -w: Whitelist file\n -b: Blacklist file\n -v: Verbose\n")


if "check" in sys.argv:
    if "-h" in sys.argv:
        print_check_help()
    else:
        pass
    if "-w" in sys.argv:
        whitelist = read_file(sys.argv[sys.argv.index("-w") + 1])
    else:
        print_check_help()
        sys.exit()
    if "-b" in sys.argv:
        blacklist = read_file(sys.argv[sys.argv.index("-b") + 1])
    else:
        print_check_help()
        sys.exit()
    if "-o" in sys.argv:
        output_file = sys.argv[sys.argv.index("-o") + 1]
        bad_ips = []
        with open(output_file, 'w') as f:
            for ip in blacklist:
                if ip in whitelist:
                    with open(output_file, 'w') as f:
                        f.write(ip + "\n")
    if "-v" in sys.argv:
        print("Checking if whitelist contains blacklisted IPs...")
        for ip in blacklist:
            if ip in whitelist:
                print("Whitelist contains blacklisted IPs")
                sys.exit()
        print("Whitelist does not contain blacklisted IPs")
    else:
        pass
    
    sys.exit()

#  

# get user inputs
if "-h" in sys.argv:
    print_help()
    sys.exit()

if "-w" in sys.argv:
    whitelist = read_file(sys.argv[sys.argv.index("-w") + 1])
else:
    print_help()
    sys.exit()

if "-b" in sys.argv:
    blacklist = read_file(sys.argv[sys.argv.index("-b") + 1])
else:
    print_help()
    sys.exit()

if "-o" in sys.argv:
    output_file = sys.argv[sys.argv.index("-o") + 1]
    with open(output_file, 'w') as f:
        for ip in remove_blacklisted_ips(whitelist, blacklist):
            f.write(ip + "\n")

if "-v" in sys.argv:
    print(remove_blacklisted_ips(whitelist, blacklist))
else:
    pass
