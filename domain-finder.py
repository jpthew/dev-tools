#!/usr/bin/python3

# import modules for dns lookup and whois lookup
import dns.resolver # requires pip3 install dnspython
import sys

# create function for reverse dns lookup by ip address
def reverse_dns(ip):
    try:
        return str(dns.resolver.resolve(dns.reversename.from_address(ip), "PTR")[0])
    except:
        return None

# create function to read file of ips and use reverse_dns() function to get domain names
def get_domains_from_ips(ip_file):
    domains = []
    with open(ip_file, "r") as f:
        for line in f:
            ip = line.strip()
            domain = reverse_dns(ip)
            if domain:
                domains.append(domain)
    return domains

if "-h" in sys.argv or "--help" in sys.argv:
    print("Usage: python3 domain-finder.py <ip_file>")
    sys.exit(1)
if len(sys.argv) < 2:
    print("Error: No ip file given\n\nUsage: python3 domain-finder.py <ip_file>")
    sys.exit(1)

# print to sdtout
for domain in get_domains_from_ips(sys.argv[1]):
    print(domain)

