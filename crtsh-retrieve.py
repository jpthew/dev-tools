#!/usr/bin/python3
### NOT FINISHED DUE TO INCOMPATABILITY WITH CUSTOMER ENVIRONMENT ###
from crtsh import crtshAPI
import json
import sys
import jq

# create function to read file of domains and use crtsh API to get certificate information
# def get_cert_info(domain_file):
#     cert_info = []
#     with open(domain_file, "r") as f:
#         for line in f:
#             domain = line.strip()
#             cert_info.append(crtshAPI().search(domain))
#     return cert_info
def get_cert_info(domain_file):
    cert_info = []
    for line in domain_file:
        domain = line.strip()
        cert_info.append(crtshAPI().search(domain))


with open(sys.argv[1], "r") as f:
    domain_list = []
    for line in f:
        # if the line ends in a period (.) remove it
        if line[-1] == ".":
            line = line[:-1]
            domain_list.append(line)
        else:
            domain_list.append(line)

if "-h" in sys.argv or "--help" in sys.argv:
    print("Usage: python3 subdomain-finder.py <domain_file>")
    sys.exit(1)
# if "-o" in sys.argv: # output to file
#     output_file = sys.argv[sys.argv.index("-o") + 1]
#     with open(output_file, "w") as f:
#         for cert in get_cert_info(sys.argv[1]):
#             f.write(json.dumps(cert) + "\n")
if "-o" in sys.argv: # output to file
    output_file = sys.argv[sys.argv.index("-o") + 1]
    with open(output_file, "w") as f:
        for cert in get_cert_info(domain_list):
            f.write(json.dumps(cert) + "\n")
if len(sys.argv) < 2:
    print("Error: No domain file given\n\nUsage: python3 subdomain-finder.py <domain_file>")
    sys.exit(1)
