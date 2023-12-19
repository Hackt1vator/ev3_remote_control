#needs to be loaded seperat to the main.py programm, otherwise the subprocess library doesn't work correctly
import os
import subprocess

pwd = "maker"
proc = subprocess.Popen("/bin/bash", stdin.PIPE, stdout.PIPE)

proc.write("sudo chmod +777 " + str(os.getcwd()).removesuffix("/") + "/setup_brick.sh")

proc.write("sudo ./setup_brick.sh")
proc.write(pwd)
