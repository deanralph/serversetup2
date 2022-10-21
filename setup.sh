#!/bin/bash
# Server Setup Script

clear

echo "###################################################"
echo -e "\033[1;33m                   DEANRALPH.NET"
echo "         SERVER SETUP SCRIPT V3.0 - Back to BASH"
echo -e "\033[0m###################################################"
echo  

# Check script is being run as root user
if [ "$EUID" -ne 0 ]
  then echo -e "\033[0;31mPlease run as root"
  echo -e "\033[0m"
  exit
fi

# Downloads Dependancies
echo "Downloading Required Files..."
wget -q https://raw.githubusercontent.com/deanralph/serversetup2/main/telnet.py

#checks if user is sudo no password
echo -e "\033[1;36mChecking if user is sudo no password..."
if grep -q "dean ALL=(ALL) NOPASSWD: ALL" /etc/sudoers; then
    echo -e "\033[0;32mUser already in sudoers"
    echo -e "\033[0m"
else
    echo -e "\033[1;36mSetting sudo without password..."
    echo "Taking backup of etc/sudoers"
    cp /etc/sudoers /etc/sudoers.backup
    if test -f "/etc/sudoers.backup"; then
        echo -e "\033[0;32mbackup successfull."
        echo -e "\033[0m"
    fi
    echo "dean ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
    if grep -q "dean ALL" /etc/sudoers; then
        echo -e "\033[0;32mAdded to sudoers successfully"
        echo -e "\033[0m"
    else
        echo -e "\033[0;31mFailed to set up are you running as root?"
        echo -e "\033[0m"
        exit
    fi
fi

apt update -y

echo -e "\033[1;33mInstalling requirted apps"
echo -e "\033[0m"
apt install qemu-guest-agent openssh-server nano -y

apt upgrade -y

echo -e "\033[0;95mSo you want to bind the MAC of this machine? y/n\033[0m"

read varBind

if [ $varBind == "y" ]; then
    /bin/python3 telnet.py
else
    echo "Skipping Bind"
    echo
fi

echo "Cleaning up"
rm telnet.py
