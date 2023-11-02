#!/usr/bin/python3

import sys
import ssl
import socket
import json

def get_cert_info(domain_file): # read file and return certificate information
    cert_info = []
    try: # check if domain_file exists
        open(domain_file, "r")
    except:
        print("Error: " + domain_file + " does not exist")
        sys.exit(1)
    with open(domain_file, "r") as f:
        for line in f:
            verbose = False
            if "-v" in sys.argv or "--verbose" in sys.argv:
                verbose = True
            output_connect = False
            if "-o" in sys.argv:
                output_connect = True
            domain = line.strip()
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                try:
                    s.connect((domain, 443))
                    if verbose == True:
                        print("Connected to " + domain)
                    if output_connect == True:
                        output_file = sys.argv[sys.argv.index("-o") + 1]
                        with open(output_file, "a") as f:
                            f.write("+ " + domain + "\n")
                except:
                    if verbose == True:
                        print("Failed to connect to " + domain)
                    if output_connect == True:
                        output_file = sys.argv[sys.argv.index("-o") + 1]
                        with open(output_file, "a") as f:
                            f.write("- " + domain + "\n")
                    continue
                cert = s.getpeercert()
                cert_info.append(cert)
    return cert_info

def helppage(): # help page
    print(
    """Usage: python3 certscan.py <domain_file>

This script scans a list of domains for SSL/TLS certificates and outputs the information depending on flags set.
It is an alternative to more louder tools such as nmap and sslscan.

Flags:
    -o <output_file>    Output domain connection status to file instead of stdout 
                        --  "+" for success, "-" for failure
    -oC <output_file>   Output raw certs to file instead of stdout
    -t <float>          Set custom timeout in seconds for socket connections (Default 2 seconds) 
                        --  Usage: 
                                -t 5 (for 5 seconds)
                                -t 0.5 (for 0.5 seconds)
    -v, --verbose       Verbose output
    -h, --help          Display this help message""")

if "-h" in sys.argv or "--help" in sys.argv:
    helppage()
    sys.exit(1)
if "-t" in sys.argv: # set timeout
    socket_timeout = float(sys.argv[sys.argv.index("-t") + 1])
    socket.setdefaulttimeout(socket_timeout)
else:
    socket.setdefaulttimeout(2.0)
if "-oC" in sys.argv: # output raw certs to file
    output_file = sys.argv[sys.argv.index("-oC") + 1]
    with open(output_file, "w") as f:
        for cert in get_cert_info(sys.argv[1]):
            f.write(json.dumps(cert) + "\n")
else: 
    if "-v" in sys.argv:
        for cert in get_cert_info(sys.argv[1]):
            print("\n" + json.dumps(cert))
    else: get_cert_info(sys.argv[1])