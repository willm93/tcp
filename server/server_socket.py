import socket

class ServerSocket:
    def __init__(self, addr):
        self.addr = addr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(addr)
        self.socket.listen()

    def fileno(self):
        return self.socket.fileno()

    def close(self):
        self.socket.close()

    def on_read(self):
        socket, addr = self.socket.accept()
        response = {'type': 'new_conn', 'addr': addr, 'socket': socket}
        return response
    
