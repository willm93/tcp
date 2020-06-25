#! /usr/bin/env python3

import select
import socket
import curses
from curses import wrapper

from connection import Connection
from client_ui import ClientUI

HEADERSIZE = 64
ENCODING = 'utf-8'

class Client:
    def __init__(self, connection, ui):
        self.connection = connection 
        self.ui = ui
    
    def run(self):
        try:
            while True:
                readers, _, _, = select.select([self.ui, self.connection], [], [])
                for reader in readers:
                    response = reader.on_read()
                    self.handle_response(response)
        finally:
            self.disconnect()

    def handle_response(self, response):
        if response['type'] == 'new_msg':
            self.ui.update_chat(response['msg'])
        elif response['type'] == 'send_msg':
            self.connection.send(response['msg'])
        elif response['type'] == 'command':
            self.connection.send(response['command'])
            self.process_command(response['command'])
        elif response['type'] == 'close_conn':
            self.disconnect()
        else:
            pass

    def process_command(self, command):
        if command == "::E":
            self.disconnect()

    def disconnect(self):
        self.connection.close()

            

def main(stdscr):
    input_window = curses.newwin(5, curses.COLS, curses.LINES -5, 0)
    client_ui = ClientUI(stdscr, input_window) 
    ip = '127.0.1.1'
    port = 3000
    connection = Connection((ip,port), ENCODING, HEADERSIZE)

    client = Client(connection, client_ui)
    client.run()

if __name__ == '__main__':
    wrapper(main)
