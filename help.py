import numpy as np
import cv2
import win32gui
import win32con
import win32ui
import re
from time import sleep

def FindWindow_bySearch(pattern):
    window_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), window_list)
    for each in window_list:
        if re.search(pattern, win32gui.GetWindowText(each)) is not None:
            return each

def getWindow_W_H(hwnd):

    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = 360
    height = 40
    return (left, top, width, height)

def getWindow_Img(hwnd):
    s = win32gui.GetWindowLong(hwnd,win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, s|win32con.WS_EX_LAYERED)

    show = win32gui.IsIconic(hwnd)

    if show == 1: 
        win32gui.SystemParametersInfo(win32con.SPI_SETANIMATION, 0)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_ALPHA)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)    
        x, y, width, height = getWindow_W_H(hwnd)        

    hwindc = win32gui.GetWindowDC(hwnd)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()

    x, y, width, height = getWindow_W_H(hwnd)

    if show == 1: win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM, x, y, width, height, win32con.SWP_NOACTIVATE)

    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0 , -10), (width, height), srcdc, (145, 215), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype="uint8")
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    if show == 1 :
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
        win32gui.SystemParametersInfo(win32con.SPI_SETANIMATION, 1)

    return img





hwnd = FindWindow_bySearch("天堂2M助手")

while True:
    sleep(0.03)
    frame = getWindow_Img(hwnd)
    cv2.imshow("screen box", frame)
    k = cv2.waitKey(30)&0xFF #64bits! need a mask
    if k ==27:
        cv2.destroyAllWindows()
        break