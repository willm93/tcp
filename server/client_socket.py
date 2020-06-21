import socket

class ClientSocket:
    def __init__(self, addr, socket, encoding, headersize):
        self.addr = addr
        self.socket = socket
        self.encoding = encoding
        self.headersize = headersize

    def on_read(self):
        header_bytes = self.socket.recv(self.headersize)

        if not len(header_bytes):
            response = {'type': 'closed_conn', 'addr': self.addr}
            return response

        msg_len = int(self.decode(header_bytes))
        msg_bytes = self.socket.recv(msg_len)

        if not len(msg_bytes):
            response = {'type': 'blank_msg', 'addr': self.addr}
            return response
        
        if self.decode(msg_bytes)[:2] == "::":
            response = {'type': 'command', 'addr': self.addr, 'command': self.decode(msg_bytes)}
            return response

        response = {'type': 'new_msg', 'addr': self.addr, 'msg_bytes': msg_bytes}
        return response

    def send(self, msg_bytes):
        header_bytes = self.encode(f"{len(msg_bytes):<{self.headersize}}")
        self.socket.send(header_bytes + msg_bytes)

    def fileno(self):
        return self.socket.fileno()

    def close(self):
        self.socket.close()
    
    def decode(self, msg_bytes):
        return msg_bytes.decode(self.encoding)

    def encode(self, msg):
        return msg.encode(self.encoding)

