from ctypes import byref, c_uint, c_ulong, sizeof, Structure, windll
import random
import sys
import time
import win32api

class LASTINPUTINFO(Structure):
    fields_ = [('cbSize', c_uint), ('dwTime', c_ulong)]

def get_last_input():
    struct_lastinputinfo = LASTINPUTINFO()
    struct_lastinputinfo.cbSize = sizeof(LASTINPUTINFO) # Holds the timestamp of last input.
    windll.user32.GetLastInputInfo(byref(struct_lastinputinfo))
    run_time = windll.kernel32.GetTickCount() # Determines how long the system has been running. 
    elapsed = run_time - struct_lastinputinfo.dwTime
    print(f"[*] It's been {elapsed} milliseconds since the last event.")
    return elapsed

# Used to test the above code.
#while True:
#    get_last_input()
#    time.sleep(1)

class Detector:
    def __init__(self):
        self.double_clicks = 0
        self.keystrokes = 0
        self.mouse_clicks = 0

    def get_key_press(self):
        for i in range(0, 0xff): # Iterate over the range of valid input keys.
            state = win32api.GetAsyncKeyState(i) # Checks if a valid input key has been pressed.
            if state & 0x0001: # If state & 0x0001 is truthy...
                if i == 0x1: # Check if its value is 0x1, which = virtual key code for left-mouse click.
                    self.mouse_clicks += 1 # If so, add mouse click to count.
                    return time.time() # If so, record time for time calcs.
                elif i > 32 and i < 127: # Check for Ascii key presses.
                    self.keystrokes += 1 # If so, count keystroke. Could add record time, would be noisy.
        return None

    def detect(self):
        previous_timestamp = None
        first_double_click = None
        double_click_threshold = 0.35

        max_double_clicks = 10
        max_keystrokes = random.randint(10,25)
        max_mouse_clicks = random.randint(5,25)
        max_input_threshold = 30000

        last_input = get_last_input()
        if last_input >= max_input_threshold:
            sys.exit(0)

        detection_complete = False
        while not detection_complete:
            keypress_time = self.get_key_press() # Check for mouse clicks of key presses.
            if keypress_time is not None and previous_timestamp is not None:
                elapse = keypress_time - previous_timestamp # Calculate elapse time between input.

                if elapsed <= double_click_threshold: # Compare elapse time to threshold to determine if double click.
                    self.mouse_clicks -= 2
                    self.double_clicks += 1
                    if first_double_click is None:
                        first_double_click = time.time()
                    else:
                        if self.double_clicks >= max_double_clicks: # Checking to see if double clicks are dubious.
                            if (keypress_time - first_double_click <= # If maximum clicks and rapid succession, confirm dubious.
                                (max_double_clicks*double_click_threshold)):
                                sys.exit(0)
                if (self.keystrokes >= max_keystrokes and # Checks to see if we've made it through all checks.
                    self.double_clicks >= max_double_clicks and
                    self.mouse_clicks >= max_mouse_clicks):
                    detection_complete = True

                previous_timestamp = keypress_time
            elif keypress_time is not None:
                previous_timestamp = keypress_time

if __name__ == "__main__":
    d = Detector()
    d.detect()
    print('okay.')
