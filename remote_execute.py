"""
Script to clone http repo on remote PC
"""

#!/usr/bin/env python3
import time

import paramiko
import sys
import re

# Check if server IP is provided as an argument
if len(sys.argv) < 2:
    print("Usage: ./script.py SERVER_IP")
    sys.exit(1)

# Extract server IP from the argument
SERVER_IP = sys.argv[1]

# Define other variables
SERVER_USER = "root" # can be any user
SSH_KEY_PATH = "path_to_ssh_key"
REPO_URL = 'url_to_clone_your_repo_on_remote_server'
PASSWORD = "http_password" # it is required in case of clone repo using http


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=SERVER_IP, username=SERVER_USER, key_filename=f'{SSH_KEY_PATH}')
channel = ssh.invoke_shell()


def run_cmd(cmd, exp_prompt):
    channel.send(cmd)
    while True:
        if channel.recv_ready():
            break
    output = ""
    while not re.search(".*" + exp_prompt, output):
        resp = channel.recv(9999).decode("utf-8")
        output += resp
        time.sleep(1)
    print(output)


run_cmd("pwd\n", ":~#")
run_cmd("git config --global user.name 'your_git_user'\n", ":~#")
run_cmd("git config --global user.email 'your_git_email@example.com'\n", ":~#")

# Clone repo
run_cmd('git clone ' + REPO_URL + '\n', ":~#")

time.sleep(3)

buff = ''
while not re.search("Password for.*:", buff):
    resp = channel.recv(9999).decode("utf-8")
    buff += resp

channel.send(PASSWORD + "\n")
output = ""
while True:
    if channel.recv_ready():
        break
while not re.search(".*:~#", output):
    resp = channel.recv(9999).decode("utf-8")
    output += resp
    time.sleep(1)

print(buff)
print(output)
