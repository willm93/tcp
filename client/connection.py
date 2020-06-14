import socket

class Connection:
    def __init__(self, ip, port, encoding, headersize):
        self.ip = ip
        self.port = port
        self.encoding = encoding
        self.headersize = headersize

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.socket.connect((ip, port))

    def fileno(self):
        return self.socket.fileno()

    def close(self):
        return self.socket.close()

    def encode(self, msg):
        return msg.encode(self.encoding)

    def decode(self, msg):
        return msg.decode(self.encoding)

    def send(self, msg):
        msg_bytes = self.encode(msg)
        header_bytes = self.encode(f"{len(msg_bytes):<{self.headersize}}")
        self.socket.send(header_bytes + msg_bytes)

    def on_read(self):
        header_bytes = self.socket.recv(self.headersize)

        if not len(header_bytes):
            response = {'type': 'closed_conn'}
            return response

        msg_len = int(self.decode(header_bytes))
        msg = self.decode(self.socket.recv(msg_len))
        response = {'type': 'new_msg', 'msg': msg}
        return response
