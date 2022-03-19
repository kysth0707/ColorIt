import pyautogui
import PIL.ImageGrab
import keyboard
#from win10toast import ToastNotifier
#from plyer import notification
from threading import Thread
import clipboard
from ctypes import windll
import pygame
#import math
#import os
import time
import win32api
#import win32con
import win32gui

def CaptureIt():
    global CaptureList, CaptureEnd,CaptureProgress
    image = PIL.ImageGrab.grab().load()
    xx = x
    yy = y
    for xp in range(0, 40):
        for yp in range(0, 20):
            #color = get_pixel_color(xx + xp - 10, yy + yp - 5)
            color = image[xx + xp - 20, yy + yp - 10]
            CaptureList[xp][yp] = color
            CaptureProgress += 1
    CaptureEnd = True
    

def showtoast():
    pyautogui.confirm(title='[ ColorIt ]',text='클립보드에 복사되었습니다. ctrl + v')
##    notification.notify("[ ColorIt ]","클립보드에 복사되었습니다. ctrl + v")
##    toaster.show_toast("[ ColorIt ]",
##                       "클립보드에 복사되었습니다. ctrl + v",
##                       icon_path = None,
##                       duration = 3,
##                       threaded = False)

def rgb_to_hex(r, g, b):
    r, g, b = int(r), int(g), int(b)
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

def get_pixel_color(i_x, i_y):
    i_desktop_window_id = win32gui.GetDesktopWindow()
    i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
    long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
    i_colour = int(long_colour)
    win32gui.ReleaseDC(i_desktop_window_id,i_desktop_window_dc)
    return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)

##from win32api import GetSystemMetrics

MonitorWidth = win32api.GetSystemMetrics(0)
MonitorHeight = win32api.GetSystemMetrics(1)

pygame.init()

sysfont=pygame.font.SysFont("malgungothic",20)

screen_width = 300
screen_height = 100
screen=pygame.display.set_mode((screen_width,screen_height))#, pygame.NOFRAME)

fuchsia = (0, 0, 0)  # Transparency color

# Create layered window
##hwnd = pygame.display.get_wm_info()["window"]
##win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
##                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
## Set window transparency color
##win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
##
SetWindowPos = windll.user32.SetWindowPos
x=0
y=0
SetWindowPos(pygame.display.get_wm_info()['window'], -1, x, y, 0, 0, 0x0001)

run = True

                
#hdc = windll.user32.GetDC(0)

lastf8 = 0
lasttoast = 0
#print(time.time())

IsCaptured = False
CaptureEnd = True
CaptureProgress = 0

CaptureList = [[0 for i in range(40)] for j in range(40)] 
#CaptureList = 

while run:

##    x, y = pyautogui.position()
##
##    if(x < MonitorWidth / 2):
##        x += 30
##    else:
##        x -= 330
##        
##    if(MonitorHeight - y < 100):
##        y = MonitorHeight - 100
##    #print(MonitorHeight - y)
    #SetWindowPos(pygame.display.get_wm_info()['window'], -1, x, y, 0, 0, 0x0001)


    x, y = pyautogui.position()
    color = get_pixel_color(x, y)
    savecolor = color

    #screen.set_at((x + 1, y + 1), (0, 0, 0))
    #print(color)

    screen.fill(color)

    r,g,b = color
    r += 125
    g += 125
    b += 125
    r %= 256
    g %= 256
    b %= 256
    #print(r,g,b)

    if keyboard.is_pressed('f7'):
        if time.time() - lasttoast > 1:
            lasttoast = time.time()
            r,g,b = savecolor
            print(rgb_to_hex(r,g,b))
            clipboard.copy(str(rgb_to_hex(r,g,b))+" "+str((r,g,b)))
            #showtoast("ㅎㅇ","ㅇㅇ")
            temp=Thread(target=showtoast)
            temp.start()
        
        

    if keyboard.is_pressed('f8'):
        if time.time() - lastf8 > 0.4:
            lastf8 = time.time()

            #if not IsCaptured:
            #IsCaptured = False
            #print("캡쳐 중지")

            IsCaptured = True
            print("캡쳐")
            CaptureEnd = False
            CaptureProgress = 0
            temp=Thread(target=CaptureIt)
            temp.start()
##                for xp in range(0, 20):
##                    for yp in range(0, 10):
##                        color = get_pixel_color(x + xp - 10, y + yp - 5)
##                        CaptureList[xp][yp] = color
##                        for xx in range(0, 20):
##                            for yy in range(0, 20):
##                                screen.set_at((xp * 20 + xx, yp * 20 + yy), color)

##    for xp in range(0, 3):
##        for yp in range(0, 3):
##            color = get_pixel_color(x + xp - 1, y + yp - 1)
##            for xx in range(0, 20):
##                for yy in range(0, 20):
##                    screen.set_at((xp * 20 + xx, yp * 20 + yy), color)

    if IsCaptured and CaptureEnd:
        for xp in range(0, 40):
            for yp in range(0, 20):
                color = CaptureList[xp][yp]
                for xx in range(0, 10):
                    for yy in range(0, 10):
                        screen.set_at((xp * 5 + xx, yp * 5 + yy), color)
    color = savecolor
    truer,trueg,trueb = savecolor

    text=sysfont.render(str(truer),True,(r, g, b), color)
    screen.blit(text,(250, 0))
    text=sysfont.render(str(trueg),True,(r, g, b), color)
    screen.blit(text,(250, 30))
    text=sysfont.render(str(trueb),True,(r, g, b), color)
    screen.blit(text,(250, 60))

    text=sysfont.render(str(trueb),True,(r, g, b), color)
    screen.blit(text,(250, 60))

    text=sysfont.render(str(pyautogui.position()),True,(r, g, b), color)
    screen.blit(text,(0, 0))

    if not CaptureEnd:
        txt=str(CaptureProgress / 2)+" % 캡쳐 완료"

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run=False
            print("close")
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()

        elif event.type==pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if time.time() - lasttoast > 1:
                    lasttoast = time.time()
                    r,g,b = savecolor
                    print(rgb_to_hex(r,g,b))
                    clipboard.copy(str(rgb_to_hex(r,g,b))+" "+str((r,g,b)))
                    #showtoast("ㅎㅇ","ㅇㅇ")
                    temp=Thread(target=showtoast)
                    temp.start()
                
    
    
#	exit()

