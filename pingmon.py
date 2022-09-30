# Batch Ping Monitor by Dakoda McCoy
# 09/10/2021

from termcolor import colored
from datetime import datetime, date
import subprocess
import time
import os
import sys
import cursor

# Supresses Traceback Errors
sys.tracebacklimit = 0

# Sets Console Window Title
title = input("Enter Description: ")
os.system("title " + title)
cursor.hide()


# Assigns script current directory to variable
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

# Opens NUL for redirected ping messages
f = open('nul', 'w')

# Initilizes list of down hosts
down_hosts = []

# Gets list filename from user
def getFileName():
    file = input("Enter list filename: ")
    try:
        open(os.path.join(dirname, file), "r")
        return file
    except FileNotFoundError:
        print("File name does not exist.")
        return getFileName()

def getDelay():
    delay = input("Enter ping delay (Default 1s): ")
    try:
        if delay:
            return int(delay)
        else:
            return 1
    except ValueError:
        print("Must be an integer.")
        return getDelay()
        

# Opens file and raises an error if file does not exist
def openFile(file):
    try:
        hosts = open(os.path.join(dirname, file), "r")
        return hosts
    except FileNotFoundError:
        print("File name does not exist.")
        file = getFileName()
        return openFile(file)
        

def main():
    # Pings given host twice and outputs up if host is down
    # Logs responses in the log file
    file = getFileName()
    delay = getDelay()
    count = 1
    
    print("\n")

    while True:
        hosts = openFile(file)
        
        for host in hosts:
            host = host.strip()
        
            print(file + " | " + str(len(down_hosts)) + " currently down hosts | " + "Currently pinging: " + colored(host, "cyan"), end="\r")
            time.sleep(.5)
            print(file + " | " + str(len(down_hosts)) + " currently down hosts | " + "Currently pinging: " + colored(host, "cyan") + ".", end="\r")
            time.sleep(.5)
            print(file + " | " + str(len(down_hosts)) + " currently down hosts | " + "Currently pinging: " + colored(host, "cyan") + "..", end="\r")
            time.sleep(.5)
            print(file + " | " + str(len(down_hosts)) + " currently down hosts | " + "Currently pinging: " + colored(host, "cyan") + "...", end="\r")
            time.sleep(.5)
            sys.stdout.write("\033[K")

            result = subprocess.call(["ping", "-n", "2", host], stdout=f)

            if result == 0:
                if host in down_hosts:
                    down_hosts.remove(host)
                    
                print(file + " | " + str(len(down_hosts)) + " currently down hosts | " + "Currently pinging: " + colored(host, "cyan") + "... " + colored("OK", "green"), end="\r")
                time.sleep(delay)
                sys.stdout.write("\033[K")

            else:
                if host not in down_hosts:
                    down_hosts.append(host)
                    
                dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                today = date.today().strftime("%m%d%Y")
                
                print(dt + " " + colored("Loop Count:", "green") + colored(str(count), "green") + " " + colored(host, "cyan") + " is " + colored("down", "red"))
                with open(today + "pingmon.log", "a") as log:
                    log.write(dt +  " Loop Count: " + str(count) + " " + host + " is down\n")
                continue

        #if len(down_hosts) > 0:
        #    with open(today + "pingmon.log", "a") as log:
        #        log.write("\n" + "Loop Count " + str(count) + " down hosts:\n")
        #        for host in down_hosts:
        #            log.write(host + " \n")
        #        log.write("\n")
        count+=1
        
if __name__=="__main__":
    main()