import socket
import os
import base64

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))
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
        print("Data: "+str(data))
        client.send("Ok".encode())