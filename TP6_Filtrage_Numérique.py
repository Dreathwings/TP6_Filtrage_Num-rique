#!"C:\ProgramData\radioconda\python.exe"
# -*- coding: utf-8 -*-
# pyinstaller --icon=ressource\onde-sonore.ico TP6_Filtrage_Numérique.py
import os
import subprocess
import threading
import ctypes  # An included library with Python install.

path = os.getcwd()
path = path.replace("dist\\TP6_Filtrage_Numérique", 'UI.py')
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
subprocess.run(["C:/ProgramData/radioconda/python.exe", path],
               startupinfo=startupinfo)

def Mbox(title, text, style):
    threading.Thread(
        target=lambda: ctypes.windll.user32.MessageBoxW(0, text, title, style)
    ).start()
bob = threading.Thread(target=Mbox('Information', 
"""Faut attendre python c'est lent,
ça peut prendre jusqu'à 20 secondes si vous avez un grille-pain;
sinon fermer puis relancer

Cordialement 

Pas la direction""", 0))
bob.setDaemon(True)
bob.run()
