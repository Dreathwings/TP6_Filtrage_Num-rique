#!"C:\ProgramData\radioconda\python.exe"
# -*- coding: utf-8 -*-
import os
import subprocess
import threading
import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    threading.Thread(
        target=lambda: ctypes.windll.user32.MessageBoxW(0, text, title, style)
    ).start()
threading.Thread(target=Mbox('Information', 
     """Faut attendre python c'est lent du cul,
ça peux prendre jusqu'à 10 secondes si vous avez un grille pain,
sinon relancer

Cordialement 

Pas la direction""", 0)).run()

path = os.getcwd()
path = path.replace("dist\\TP6_Filtrage_Numérique",'UI.py')
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
subprocess.run(["C:/ProgramData/radioconda/python.exe", path],startupinfo=startupinfo)