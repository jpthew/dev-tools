#!/usr/bin/python3
# import requirements for aws cli
# import database for storing credentials and information
import boto3
import os
import sys
import argparse
import subprocess
import datetime
import re
import sqlite3

def import_aws_keys():
    # import aws keys
    print("Enter AWS Access Key ID:")
    access_key = input()
    print("Enter AWS Secret Access Key:")
    secret_key = input()
    print("Enter AWS temporary session token (if applicable):")
    session_token = input()   
    print("Enter AWS Region:")
    region = input()
    # set aws keys as environment variables
    os.environ["AWS_ACCESS_KEY_ID"] = access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = secret_key
    os.environ["AWS_SESSION_TOKEN"] = session_token
    os.environ["AWS_DEFAULT_REGION"] = region
    

def import_aws_keys_from_file():
    #check if on windows machine
    if sys.platform == "win32":
        # check if aws keys file exists
        if os.path.isfile("%USERPROFILE%\.aws\credentials"):
            credentials_file = open("%USERPROFILE%\.aws\credentials", "r")
            credentials = credentials_file.readlines()
            credentials_file.close()
            # check if multiple profiles exist
            if len(credentials) > 4:
                print("Multiple profiles detected. Please select a profile:")
                # print all profiles delineated by [profile_name]
                for i in range(0, len(credentials)):
                    if credentials[i].startswith("["):
                        print(credentials[i].strip())
                aws_profile = input()
                # set aws profile as environment variable
                for i in range(0, len(credentials)):
                    if aws_profile in credentials[i]:
                        for i in range(i, i+3):
                            os.environ[credentials[i].split("=")[0].strip()] = credentials[i].split("=")[1].strip()
            # if only one profile exists, set that profile as environment variable
            else:
                for i in range(0, len(credentials)):
                    os.environ[credentials[i].split("=")[0].strip()] = credentials[i].split("=")[1].strip()
        else:
            print("AWS credentials file not found. Please enter AWS credentials manually.")
            import_aws_keys()
    # if not on windows machine, assume linux
    else:
        # check if aws keys file exists
        if os.path.isfile("~/.aws/credentials"):
            credentials_file = open("~/.aws/credentials", "r")
            credentials = credentials_file.readlines()
            credentials_file.close()
            # check if multiple profiles exist
            if len(credentials) > 4:
                print("Multiple profiles detected. Please select a profile:")
                # print all profiles delineated by [profile_name]
                for i in range(0, len(credentials)):
                    if credentials[i].startswith("["):
                        print(credentials[i].strip())
                aws_profile = input()
                # set aws profile as environment variable
                for i in range(0, len(credentials)):
                    if aws_profile in credentials[i]:
                        for i in range(i, i+3):
                            os.environ[credentials[i].split("=")[0].strip()] = credentials[i].split("=")[1].strip()
            # if only one profile exists, set that profile as environment variable
            else:
                for i in range(0, len(credentials)):
                    os.environ[credentials[i].split("=")[0].strip()] = credentials[i].split("=")[1].strip()
        else:
            print("AWS credentials file not found. Please enter AWS credentials manually.")
            import_aws_keys()  

def validate_keys():
    # check if aws keys are valid
    try:
        sts = boto3.client('sts')
        sts.get_caller_identity()
        print("AWS keys are valid.")
    except:
        print("AWS keys are borked. Please try again.")
        import_aws_keys()

def get_account_id():
    # get account id
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()["Account"]
    return account_id

def get_account_user():
    # get account user
    sts = boto3.client('sts')
    account_user = sts.get_caller_identity()["Arn"].split("/")[1]
    return account_user

def start_db():
    # start database
    print("Starting database...")
    conn = sqlite3.connect('aws_keys.db')
    c = conn.cursor()
    # create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS aws_keys
                (db_key_id integer,key_name text, aws_access_key_id text, aws_secret_access_key text, aws_session_token text, aws_region text, account_id text, account_user text, datetime text, expiration text, remote_server text, hops text, stale text)''')
    conn.commit()
    return conn

def ec2_server_get_tokens():
    print("Is this server available to the internet? (y/n)")
    if input().lower() == "y":
        print("Enter EC2 server IP address:")
        # fail if not valid IP address
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", input()):
            remote_server = input()
            hops = 0
        else: 
            print("Invalid IP address.")
    else:
        print("Enter EC2 server IP address:")
        remote_server = input()
        print("Enter number of hops to EC2 server:")
        hops = input()
        for i in range(0, hops):
            print("Enter IP address of hop " + str(i) + ":")
            hop = input()
            hops = hops + " -> " + hop

def check_if_stale():
    # import keys aws_access_key, aws_secret_access_key, aws_session_token, aws_region
    conn = sqlite3.connect('aws_keys.db')
    c = conn.cursor()
    for i in len(c.execute("SELECT db_key_id FROM aws_keys")):
        # check if key is stale
        if datetime.datetime.now() > c.execute("SELECT expiration FROM aws_keys WHERE db_key_id = " + str(i)):
            c.execute("UPDATE aws_keys SET stale = 'True' WHERE db_key_id = " + str(i))
        else:
            c.execute("UPDATE aws_keys SET stale = 'False' WHERE db_key_id = " + str(i))
    conn.commit()

def get_stale_keys():
    # import keys aws_access_key, aws_secret_access_key, aws_session_token, aws_region
    conn = sqlite3.connect('aws_keys.db')
    c = conn.cursor()
    stale_keys = []
    for i in len(c.execute("SELECT key_name FROM aws_keys WHERE stale = 'True'")):
        stale_keys.append(i)
    return stale_keys

def refresh_key():
    conn = sqlite3.connect('aws_keys.db')
    c = conn.cursor()
    print("Enter key name to refresh:")
    keys = (c.execute("SELECT key_name FROM aws_keys"))
    for i in range(0, len(keys)):
        print(keys[i])
    key_name = input()
    # check if key exists
    if key_name in keys:
        pass
    else:
        print("Key not found.")
        refresh_key()

