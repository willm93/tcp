import sys
import curses

class ClientUI:
    def __init__(self, chat_window, input_window):
            self.chat_window = chat_window
            self.input_window = input_window
            self.current_line = 0
            self.chat_window.refresh()
            self.input_window.refresh()

    def on_read(self):
        msg = sys.stdin.readline().strip()

        if msg[:2] == "::":
            response = {'type': 'command', 'command': msg}
            return response

        response = {'type': 'send_msg', 'msg': msg}
        return response

    def fileno(self):
        return sys.stdin.fileno()

    def update_chat(self, msg):
        self.chat_window.addstr(self.current_line, 2, msg)
        self.current_line += 1
        self.chat_window.refresh()

    def clear_input(self):
        pass
