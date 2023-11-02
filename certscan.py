#!/usr/bin/python3

import sys
import ssl
import socket
import json

# read file and return certificate information
def get_cert_info(domain_file):
    cert_info = []
    with open(domain_file, "r") as f:
        for line in f:
            verbose = False
            if "-v" in sys.argv or "--verbose" in sys.argv:
                verbose = True
            domain = line.strip()
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                try:
                    s.connect((domain, 443))
                    if verbose == True:
                        print("Connected to " + domain)
                except:
                    if verbose == True:
                        print("Failed to connect to " + domain)
                    continue
                cert = s.getpeercert()
                cert_info.append(cert)
    return cert_info

if "-h" in sys.argv or "--help" in sys.argv:
    print("Usage: python3 certscan.py <domain_file>\n\nFlags:\n    -o <output_file>    Output to file instead of stdout\n   -v, --verbose       Verbose output\n    -h, --help          Display this help message")
    sys.exit(1)
if "-o" in sys.argv: # output to file
    output_file = sys.argv[sys.argv.index("-o") + 1]
    with open(output_file, "w") as f:
        for cert in get_cert_info(sys.argv[1]):
            f.write(json.dumps(cert) + "\n")
else:
    for cert in get_cert_info(sys.argv[1]):
        print(json.dumps(cert))