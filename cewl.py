#!/usr/sbin/python3
#
#
# COVERT TO ARGPARSE #
import sys
import os
import subprocess
import threading
import datetime
import argparse
import tqdm

def helppage():
    print(
    """
Usage: python3 cewlspider.py -iL <input_file>

Flags:
    -o <output_file>    Output to file instead of stdout
    -h, --help          Show this help page
    -i <input_file>    Input file of domains to spider and cewl
    
    """)
def current_day_formatted(): # get current day in mm-dd-yyyy format
    return datetime.datetime.now().strftime("%m-%d-%Y")

def check_reqs(): # validate/install required tools
    try:
        subprocess.check_output(["gospider", "-h"])
    except:
        print("***Error: gospider is not installed***\n\nInstall now? (y/n)")
        if input().lower() == "y":
            subprocess.run(["sudo", "apt", "install", "gospider", "-y"])
        else:
            sys.exit(1)
        try:
            subprocess.check_output(["cewl", "-h"])
        except:
            print("***Error: cewl is not installed***\n\nInstall now? (y/n)")
            if input().lower() == "y":
                subprocess.run(["sudo", "apt", "install", "cewl", "-y"])
            else:
                sys.exit(1)
        sys.exit(1)
    try:
        subprocess.check_output(["cewl", "-h"])
    except:
        print("***Error: cewl is not installed***\n\nInstall now? (y/n)")
        if input().lower() == "y":
            subprocess.run(["sudo", "apt", "install", "cewl", "-y"])
        else:
            sys.exit(1)


def run_gospider(shared_data):
    try:
        shared_data['gospider_borked'] = subprocess.run(["gospider", "-S", args.input, "--depth", "3", "-o", "/tmp/" + current_day_formatted() + "-gospider"])
    except:
        print("Error: gospider failed for some reason")
        sys.exit(1)

def main():
    check_reqs()
    try: #check if args.input file exists
        open(args.input, "r")
    except:
        print("Error: " + args.input + " does not exist")
        sys.exit(1)

    # gospider section
    shared_data = {}
    gospider_thread = threading.Thread(target=run_gospider, args=(shared_data,))
    gospider_thread.start()
    if args.verbose == True:
        print(gospider_thread.is_alive())
        # print stdout of gospider_borked pipe until finished
        while gospider_thread.is_alive():
            for line in iter(shared_data.get('gospider_borked', {}).get('stdout', '').strip('\n')):
                print(line)
    else:
        print("Running gospider...") # Could make this bigger later
        print("This may take a while...")
    gospider_thread.join()
    print("gospider finished") # Could make this bigger later

    # cewl section
    

                





# args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input file of domains to spider and cewl")
parser.add_argument("-o", "--output", help="Output to file instead of stdout")
parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
args = parser.parse_args()
main()
    