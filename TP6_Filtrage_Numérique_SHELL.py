#!"C:\ProgramData\radioconda\python.exe"
# -*- coding: utf-8 -*-
import os
import subprocess
path = os.getcwd()
path = path.replace("dist",'UI.py')
subprocess.run(["C:/ProgramData/radioconda/python.exe", path])