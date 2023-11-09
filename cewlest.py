#!/usr/sbin/python3
#
#
# NEED TO ADD STDIN SUPPORT (Need to modify all lines referencing args.input) #
import sys
import os
import subprocess
import threading
import datetime
import argparse
import re
import textwrap
import fileinput

def print_disable():
    sys.stdout = open(os.devnull, 'w')
def print_enable():
    sys.stdout = sys.__stdout__

def splash_screen():
    print("""
   ____   __        ___              _   
  / ___|__\ \      / / |    ___  ___| |_ 
 | |   / _ \ \ /\ / /| |   / _ \/ __| __|
 | |__|  __/\ V  V / | |__|  __/\__ \ |_ 
  \____\___| \_/\_/  |_____\___||___/\__|
                                         
                            by JP Thew
    """)

def current_day_formatted(): # get current day in mm-dd-yyyy format
    return datetime.datetime.now().strftime("%m-%d-%Y")

def check_reqs(): # validate/install required tools
    try:
        verbose_print("Checking for local installation of gospider and cewl")
        subprocess.check_output(["gospider", "-h"])
        verbose_print("gospider is installed")
    except:
        print("[ERROR] gospider is not installed\n\nInstall now? (y/n)")
        if input().lower() == "y":
            subprocess.run(["sudo", "apt", "install", "gospider", "-y"])
        else:
            sys.exit(1)
        try:
            subprocess.check_output(["cewl", "-h"])
            verbose_print("cewl is installed")
        except:
            print("[ERROR] cewl is not installed\n\nInstall now? (y/n)")
            if input().lower() == "y":
                subprocess.run(["sudo", "apt", "install", "cewl", "-y"])
            else:
                sys.exit(1)
        sys.exit(1)
    try:
        subprocess.check_output(["cewl", "-h"])
        verbose_print("cewl is installed")
    except:
        print("[ERROR] cewl is not installed\n\nInstall now? (y/n)")
        if input().lower() == "y":
            subprocess.run(["sudo", "apt", "install", "cewl", "-y"])
        else:
            sys.exit(1)

def verbose_print(string):
    if args.verbose == True:
        print("[VERBOSE] " + string)

def run_gospider(shared_data):
    try:
        print("[INFO] Running gospider...\n[INFO] This may take a while...") ### Could make this bigger later
        process = subprocess.run(["gospider", "-S", args.input, "--depth", "3"], capture_output=True, text=True)
        shared_data['gospider_borked'] = process
        shared_data['stdout'] = process.stdout
        verbose_print("gospider finished")
        
    except:
        print("[ERROR] gospider failed for some reason")
        sys.exit(1)

def cewl(list_part, thread_num, cewl_out):
    for line in list_part:
        verbose_print("[Thread " + str(thread_num) + "] " + "Running cewl against " + str(line))
        try:
            test = subprocess.run(["cewl", "-e", "-d0", "--ua", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5", line], capture_output=True, text=True)
            cewl_out.append(test.stdout)
        except:
            verbose_print("[ERROR] CeWL failed scan of " + line)
            pass
        verbose_print("[Thread " + str(thread_num) + "] " + "Finished cewl against " + str(line))

def split_list(list_var, n):
    k, m = divmod(len(list_var), n)
    return (list_var[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def cewl_split(num_threads, list_var):
    length = len(list_var)
    threads = []
    split = int(length / num_threads)
    verbose_print("Each thread gets " + str(split) + " URLs")
    if split == 0:
        print("[ERROR] Number of threads is too high. Lower threads or increase scope.")
        sys.exit(1)
    else: 
        parts = list(split_list(list_var, num_threads))
        cewl_out = []
    for i in range(num_threads):
        threads.append(threading.Thread(target=cewl, args=(parts[i], i, cewl_out)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    return cewl_out

def main():

    if args.quiet == True:
        print_disable()
    # check required tools
    check_reqs()
    try: #check if args.input file exists
        open(args.input, "r")
    except:
        print("[ERROR] " + str(args.input) + " does not exist")
        sys.exit(1)


    # gospider section
    shared_data = {}
    gospider_thread = threading.Thread(target=run_gospider, args=(shared_data,))
    gospider_thread.start()
    verbose_print("Is gospider thread up?: " + str(gospider_thread.is_alive()))
    gospider_thread.join()
    print("[INFO] gospider finished") ### Could make this bigger later
    gospider_list = shared_data['stdout'].split("\n")
    if args.verbose == True:
        print("[VERBOSE] Do you want to output gospider output to stdout? (y/n)")
        if input().lower() == "y":
            for line in gospider_list:
                print(line)
        else:
            print("[VERBOSE] Continuing...")
    if args.gospider_output: # Print gospider output to file
        verbose_print("Saving gospider output to " + args.gospider_output)
        with open(args.gospider_output, "w") as f:
            for line in gospider_list:
                f.write(line + "\n")

    # gospider cleanup section
    verbose_print("Cleaning up gospider output")
    gospider_list = [line.split(" ") for line in gospider_list]
    try:
        clean_list = []
        for s in gospider_list:
            for i in s:
                if i.startswith("http"):
                    clean_list.append(i)
    except:
        print("[ERROR] gospider output is not in the expected format")
        sys.exit(1)
    gospider_list = clean_list # formatted as list
    verbose_print("gospider output cleaned up")

    # cewl section
    cewl_list = []
    print("[INFO] Running cewl with " + str(args.threads) + " threads...")
    cewl_list_cleaned = []
    for line in cewl_split(args.threads, gospider_list):
        for i in line.split("\n"):
            cewl_list_cleaned.append(i)
    cewl_list_cleaned = list(set(cewl_list_cleaned))
    for line in cewl_list_cleaned: # cleaning up the final list
        if not re.search("\s", line) and not re.search("error|cewl|robin@digi.ninja", line, re.IGNORECASE):
            cewl_list.append(line)
    print("[INFO] cewl finished")

    #output cewl_list as user specified
    if args.output:
        verbose_print("[INFO] Saving cewl output to " + args.output)
        with open(args.output, "w") as f:
            for line in cewl_list:
                f.write(line + "\n")
    else:
        if args.quiet == True:
            print_enable()
        for line in cewl_list:
            print(line)

    

splash_screen()
parser = argparse.ArgumentParser(
    prog="cewlest.py", 
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
        A wrapper for gospider and a multithreaded adaptation of CeWL to spider and scrape URLs from a list of domains.
        Allows for clean output to stdout with -q/--quiet and output to file with -o/--output.
    '''), 
    epilog="Example: python3 cewlest.py -i domains.txt -o output.txt -t 5")
parser.add_argument("-i", "--input", help="Input file of domains to spider and cewl", metavar="FILE", default=sys.stdin)
parser.add_argument("-o", "--output", help="Output to file instead of stdout", metavar="FILE")
parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
parser.add_argument("-t", "--threads", help="Number of threads to use with cewl. (Default 5)", type=int, default=5, metavar="<int>")
parser.add_argument("-q, --quiet", help="Disable all output except CeWL output (Ideal for piping STDOUT)", action="store_true", dest="quiet")
parser.add_argument("--gospider-output", help="Save gospider output to a file")
args = parser.parse_args()
if args.verbose == True and args.quiet == True:
    print("[ERROR] CeWLest cannot be both verbose and quiet")
    sys.exit(1)
main()