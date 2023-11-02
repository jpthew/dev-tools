#!/usr/bin/python3

# import modules for dns lookup and whois lookup
import dns.resolver # requires pip3 install dnspython
import sys
import tqdm

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

if "-h" in sys.argv or "--help" in sys.argv: # help menu
    print("Usage: python3 domain-finder.py <ip_file>\n\nFlags:\n    -o <output_file>    Output to file instead of stdout")
    sys.exit(1)
if "-o" in sys.argv: # output to file
    output_file = sys.argv[sys.argv.index("-o") + 1]
    with open(output_file, "w") as f:
        for domain in tqdm(get_domains_from_ips(sys.argv[1])):
            f.write(domain.rstrip('.') + "\n")
else:
    for domain in tqdm(get_domains_from_ips(sys.argv[1])):
        print(domain.rstrip('.'))
if len(sys.argv) < 2: # error if no ip file given
    print("Error: No ip file given\n\nUsage: python3 domain-finder.py <ip_file>")
    sys.exit(1)

