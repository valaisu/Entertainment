import pyautogui as pag
import time
import random
import PIL.ImageGrab

#converts text thorough multple languages using google translate
#for example a food recept will give you hilarious results
#instructions: Copy the text you want to translate on your clipboard
#Make sure that:
#   - the language google translate uses (on row 63 link) corresponds to the initial language
#   - you are not using flux, or other softwares, that alter the screen colors
#   - when you write "c" in your windows search bar, the presumed software to open is chrome,
#     that it will open in fullscreen mode.


def pasteText():
    for i in range(3):
        pag.click(200, 370)
    pag.keyDown("ctrl")
    pag.press("v")
    pag.keyUp("ctrl")


def copyText():
    for i in range(3):
        pag.click(1200, 370)
    pag.keyDown("ctrl")
    pag.press("c")
    pag.keyUp("ctrl")

def pickLanguage():

    findButton()
    pag.click(random.randint(200, 1720), random.randint(400, 1050))

def up():
    pag.press("pageup")
    time.sleep(0.2)

def switch():
    pag.click(960, 280)

def findButton():
    c = PIL.ImageGrab.grab().load()
    temp = 1
    for j in range(500):
        if c[1700 - temp, 280] != (135, 138, 142):
            print(c[1700 - temp, 280])
            temp += 1
        else:
            break
    pag.click(int(1700 - temp), 280)

pag.press("win")
time.sleep(0.5)
pag.press("c")
time.sleep(0.1)
pag.press("enter")
time.sleep(2)
pag.keyDown("ctrl")
pag.press("t")
pag.keyUp("ctrl")
pag.write("https://translate.google.fi/?hl=fi&sl=fi&tl=en&op=translate")
time.sleep(0.1)
pag.press("enter")
#"https://translate.google.fi/?sl=en&tl=fi&op=translate&hl=fi"
time.sleep(4)

pasteText()
time.sleep(0.5)
pag.press("pageup")


time.sleep(2)

for i in range(30):
    up()
    pickLanguage()
    time.sleep(1)
    switch()
    time.sleep(1)
#200-1720, 400-1050
switch()
time.sleep(1)
findButton()
time.sleep(1)
pag.click(1400,1050)
