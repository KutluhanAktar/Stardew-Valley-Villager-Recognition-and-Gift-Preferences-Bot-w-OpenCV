import numpy as np
import win32gui, win32ui, win32con

class captureWindowFrame:
    def __init__(self, window_name):
        # Define the handle for the selected window.
        # Full Screen:
        # self.hwnd = win32gui.GetDesktopWindow()
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window Not Found: {}'.format(window_name))
        # Window Sizes:
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        # Adjust the window to remove unnecessary pixels:
        self.border_px = 8
        self.titlebar_px = 30
        self.w = self.w - (self.border_px * 2)
        self.h = self.h - self.titlebar_px - self.border_px
    def get_frames(self):
        # Get the frame (screenshot) data:
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.border_px, self.titlebar_px), win32con.SRCCOPY)
        # Convert the raw frame data for OpenCV:
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        # Clear the frame data:
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        # Drop the alpha channel and make the image C_CONTIGUOUS to avoid errors while running OpenCV:
        img = img[...,:3]
        img = np.ascontiguousarray(img)
        # Return:
        return img
    # List window names:
    def get_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)
    