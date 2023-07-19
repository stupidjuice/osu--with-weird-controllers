from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE

with Popen("cmd", stdout=PIPE, bufsize=1, universal_newlines=True, creationflags=CREATE_NEW_CONSOLE) as p:
    for line in p.stdout:
        print(line, end='')