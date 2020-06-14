import sys

class KeyboardInput:

    def fileno(self):
        return sys.stdin.fileno()

    def on_read(self):
        msg = sys.stdin.readline().strip()

        if msg[:2] == "::":
            response = {'type': 'command', 'command': msg}
            return response

        response = {'type': 'send_msg', 'msg': msg}
        return response

