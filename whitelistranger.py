#!/bin/python3

# import modules
import os
import sys
import ipaddress

# define functions
def read_file(filename):
    with open(filename, 'r') as f:
        ips = f.read().splitlines()
    ips_list = []
    for ip in ips:
        if "/" in ip:
            for ip in ipaddress.IPv4Network(ip):
                ips_list.append(str(ip))
        else:
            ips_list.append(ip)
    return ips_list

def remove_blacklisted_ips(whitelist, blacklist):
    for ip in blacklist:
        if ip in whitelist:
            whitelist.remove(ip)
    return whitelist

# help menu
def print_help():
    print("\nThis tool creates a list of IPs from whitelist and blacklist files, creating a clean target list. It handles CIDR notation in the input files.\nIt can also verify that a whitelist file does not include IPs from a chosen blacklist file with --verify\n\nUsage: whitelistranger.py -w whitelist.txt -b blacklist.txt -o output.txt\n\n Flags:\n\n -h: This help menu\n -w: Whitelist file\n -b: Blacklist file\n -o: Output file\n -v: Verbose (print to stdout)\n")


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
    print_
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
