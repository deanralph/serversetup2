import telnetlib
import socket
import os
import getpass

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def bindMac(octet):
    macAddr = ""
    trimmedHostname = socket.gethostname()[0:12]
    os.system('cat /sys/class/net/en*/address >> mac.txt')
    with open("mac.txt", 'r') as f:
        macAddr = f.readline()
    os.remove('mac.txt')
    draytekCLIString = f"ip bindmac add 10.0.0.{octet} {macAddr[:-1]} {trimmedHostname}"

    HOST = "10.0.0.1"
    user = "admin"

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"Account:")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    tn.write(bytes(draytekCLIString, encoding='ascii') + b"\n")
    tn.write(b"exit\n")

    tn.close

    print(tn.read_all().decode('ascii'))

def getMacs():

    ips = []
    
    draytekCLIString = f"ip bindmac show"

    HOST = "10.0.0.1"
    user = "admin"

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"Account:")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    tn.write(bytes(draytekCLIString, encoding='ascii') + b"\n")
    for x in range(1,10):
        tn.write(b"\n")
    tn.write(b"exit\n")

    tn.close
    with open('macs.txt', 'w') as f:
        f.write(tn.read_all().decode('ascii'))
    
    with open('macs.txt', 'r') as f:
        macs = []
        for line in f.readlines():
            if "IP : " in line:
                macs.append(line)
        for x in macs:
            _ = x.split(" ")
            ips.append(int(_[2].split(".")[3]))
        ips.sort()

    print(f"{bcolors.OKBLUE}Here are the currently used IPs:{bcolors.ENDC}")
    for x in ips:
        if 100 <= x < 200:
            print(f"{bcolors.WARNING}    10.0.0.{x}{bcolors.ENDC}")
    print("")

password = getpass.getpass("Please enter router password: ")
_ = getMacs()
bindMac(input("Please Enter 4th Octet: "))

os.remove('macs.txt')
