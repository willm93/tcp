#! /usr/bin/env python3

import socket
import select
import sys

from server_socket import ServerSocket
from client_socket import ClientSocket

HEADERSIZE = 64
PORT = 3000
IP = socket.gethostbyname(socket.gethostname())
ENCODING = 'utf-8'

class Server:
    def __init__(self, server_socket):
        self.server_socket = server_socket 
        self.client_sockets = []
        print(f"[INIT] Server is listening on {IP}:{PORT}")
    
    def run(self):
        try:
            print("[RUNNING]")
            while True:
                rdy_sockets, _, _ = select.select(self.all_sockets(), [], [])
                for socket in rdy_sockets:
                    response = socket.on_read()
                    self.handle_response(response)
        except Exception as e:
            print(f"[ERROR] Line {sys.exc_info()[-1].tb_lineno}: {str(e)}")
            self.shutdown()

    def handle_response(self, response):
        if response['type'] == 'new_msg':
            self.msg_broadcast(response['addr'], response['msg_bytes']) 
        elif response['type'] == 'blank_msg':
            pass
        elif response['type'] == 'command':
            self.process_command(response['addr'], response['command'])
        elif response['type'] == 'new_conn':
            self.add_client(response['addr'], response['socket'])
        elif response['type'] == 'closed_conn':
            self.remove_client(response['addr'])
        else:
            print("[HANDLE FAILED] unknown response")

    def all_sockets(self):
        return self.client_sockets + [self.server_socket]

    def add_client(self, addr, socket):
        new_client = ClientSocket(addr, socket, ENCODING, HEADERSIZE)
        self.client_sockets.append(new_client)
        self.server_broadcast(f"SERVER: {new_client.addr} has entered chat")
        print(f"[NEW CONNECTION] {new_client.addr} connected")

    def find_client(self, addr):
        for client in self.client_sockets:
            if client.addr == addr:
                return client

    def remove_client(self, addr):
        client = self.find_client(addr)
        if client:
            client.close()
            self.client_sockets.remove(client)
            self.server_broadcast(f"SERVER: {client.addr} has left chat")
            print(f"[CLOSED CONNECTION] {client.addr} disconnected")
        else:
            print(f"[REMOVE FAILED] {addr} not found")
    
    def server_broadcast(self, msg):
        msg_bytes = msg.encode(ENCODING)
        for client in self.client_sockets:
            client.send(msg_bytes)

    def msg_broadcast(self, addr, msg_bytes):
        print(f"[BROADCAST] {addr}: {msg_bytes.decode(ENCODING)}")
        for client in self.client_sockets:
            if client.addr != addr:
                client.send(msg_bytes)

    def process_command(self, addr, command):
        if command == "::E":
            self.remove_client(addr)
        else:
            client = self.find_client(addr)
            if client:
                client.send("SERVER: Unknown Command".encode(ENCODING))
                print(f"[COMMAND FAILED] unknown command from {addr}")
            else:
                print(f"[COMMAND FAILED] {addr} not found")

    def shutdown(self):
        for client in self.client_sockets:
            client.close()
        self.server_socket.close()
        print("[SHUTTING DOWN]")
        sys.exit()


if __name__ == '__main__':
    addr = (IP, PORT)
    server_socket = ServerSocket(addr)
    server = Server(server_socket)
    server.run()
