import PIL.ImageGrab
import time
import pyautogui as pag

# A bot, that nails the lumberjack telegram game.
# Has been adjusted for a zoomed out version in the browser
# Will give a score of roughly 600, while the humanly achievable
# score is maybe between 400 and 500

pag.PAUSE = 0.015#0.02

a = [161, 116, 56]
pag.moveTo(400, 900)
b = [126, 173, 79]

c = PIL.ImageGrab.grab().load()[400, 420]
print(c)
for i in range(2):
    pag.click(550, 960)
q = True
w = True
e = True
r = True
t = True
y = True
for j in range(60):
    time.sleep(0.2) #0.175
    if (PIL.ImageGrab.grab().load()[411, 737] == (161, 116, 56)):
        q = True
    else:
        q = False

    if (PIL.ImageGrab.grab().load()[411, 655] == (161, 116, 56)):
        w = True
    else:
        w = False

    if (PIL.ImageGrab.grab().load()[411, 563] == (161, 116, 56)):
        e = True
    else:
        e = False

    if (PIL.ImageGrab.grab().load()[411, 485] == (161, 116, 56)):
        r = True
    else:
        r = False

    if (PIL.ImageGrab.grab().load()[411, 400] == (161, 116, 56)):
        t = True
    else:
        t = False

    if (PIL.ImageGrab.grab().load()[411, 318] == (161, 116, 56)):
        y = True
    else:
        y = False


    if q:
        for i in range(2):
            pag.click(550, 960)
    else:
        for i in range(2):
            pag.click(400, 960)
    if w:
        for i in range(2):
            pag.click(550, 960)
    else:
        for i in range(2):
            pag.click(400, 960)
    if e:
        for i in range(2):
            pag.click(550, 960)
    else:
        for i in range(2):
            pag.click(400, 960)
    if r:
        for i in range(2):
            pag.click(550, 960)
    else:
        for i in range(2):
            pag.click(400, 960)
    if t:
        for i in range(2):
            pag.click(550, 960)
    else:
        for i in range(2):
            pag.click(400, 960)
    if y:
        for i in range(2):
            pag.click(550, 960)
    else:
        for i in range(2):
            pag.click(400, 960)
