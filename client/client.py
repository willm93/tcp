#! /usr/bin/env python3

import select
import socket
import sys

from connection import Connection
from keyboard_input import KeyboardInput

HEADERSIZE = 64
ENCODING = 'utf-8'

class Client:
    def __init__(self, ip, port, encoding, headersize):
        self.connection = Connection(ip, port, encoding, headersize)
        self.keyboard_input = KeyboardInput()
    
    def disconnect(self):
        self.connection.close()
        print("----------------------------------")
        print("Connection closed")
        sys.exit()

    def process_command(self, command):
        if command == "::E":
            self.disconnect()

    def handle_response(self, response):
        if response['type'] == 'new_msg':
            print(response['msg'])
        elif response['type'] == 'send_msg':
            self.connection.send(response['msg'])
        elif response['type'] == 'command':
            self.connection.send(response['command'])
            self.process_command(response['command'])
        elif response['type'] == 'close_conn':
            self.disconnect()
        else:
            pass
        
    def run(self):
        print(f"Connected to {self.connection.ip}:{self.connection.port}")
        print("Type '::E' and press enter to exit")
        print("----------------------------------")
        try:
            while True:
                readers, _, _, = select.select([self.keyboard_input, self.connection], [], [])
                for reader in readers:
                    response = reader.on_read()
                    self.handle_response(response)
        except BrokenPipeError as e:
            print("Connection closed")
        except Exception as e:
            print(f"Error: Line {sys.exc_info()[-1].tb_lineno}: {str(e)}")


if __name__ == '__main__':
    ip = '127.0.1.1' #input("set ip: ")
    port = 3000 #input("set port: ")
    client = Client(ip, port, ENCODING, HEADERSIZE)
    client.run()
