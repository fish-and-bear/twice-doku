import pygame as pg
import os
import filehandler as fileHandler
pg.init()

# Colors
RED = "#FE001B"
BLUE = (0, 0, 255)
DARKBLUE = (0, 47, 64)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
TWICEPINK = (215, 46, 89)
YELLOW = "#FFDB00"
YELLOW2 = "#FDD509"
YELLOW3 = "#ffd500"
DARKYELLOW = "#F6991B"
DIRTYWHITE = "#F6F6F6"
SKYBLUE = "#00E2EF"
PINK = "#FF4BA8"
DARKPINK = "#E63762"
ORANGE = "#F1C641"
DARKRED = "#b31217"
PEACH = "#CC561D"
button1 = DIRTYWHITE
button2 = DIRTYWHITE
button3 = DIRTYWHITE
button4 = DIRTYWHITE
difficulty = DARKPINK
hoverbutton = YELLOW
hoverdifficulty = SKYBLUE

# DISPLAY
WIDTH = 1000
HEIGHT = 600
HBTN1 = HEIGHT/2.5
bottommargin = HEIGHT/12

# FILES
icon = 'pictures/twice-logo.png'
gridfile = 'files/grid.json'
timefile = 'files/time.json'
scoresfile = 'files/scores.json'
settingsfile = 'files/settings.json'
optionstheme = 'themes/options.json'

# DEFAULTS
button1def = "#F6F6F6"
button2def = "#F6F6F6"
button3def = "#F6F6F6"
button4def = "#F6F6F6"
difficultydef = "#E63762"
try:
    if os.stat(settingsfile).st_size > 0:
        settings = fileHandler.json_open(settingsfile)
        volumedef = settings['volume']
        resolutiondef = settings['resolution']
        resolution_string = resolutiondef.split('x')
        WIDTH = int(resolution_string[0])
        HEIGHT = int(resolution_string[1])
        themedef = settings["theme"]
    else:
        volumedef = 50
        resolutiondef = '1000x600'
        themedef = 'CHEER UP'
except OSError:
    volumedef = 50
    resolutiondef = '1000x600'
    themedef = 'CHEER UP'

# FONTS
title = 'fonts/04B30.ttf'
text = 'fonts/Pixeboy.ttf'
header = WIDTH/2, HEIGHT/3
header2 = WIDTH/2, HEIGHT/8
headersize = WIDTH/10
headersize2 = WIDTH/20
Headersize3 = WIDTH/15
textsize = WIDTH/28
gametextsize = WIDTH/40
guidetextsize = WIDTH/65

## THEMES
# CHEER UP
cuBLUEGREEN = (122, 219, 212)
cuWHITE = (254, 255, 255)
# What is Love?
wilPINK = (248,194,200)
wilBLACK = (23,2,3)
wilRED = (197,28,16)
# Dance the Night Away
dtnaLIGHTBLUE = (53,231,228)
dtnaWHITE = DIRTYWHITE
dtnaYELLOW = (253,230,130)
dtnaBLUE = (227, 255, 253)
# Yes or Yes
yoyLIGHTPURPLE = (255,204,255)
yoyDARKPURPLE = (71, 10, 79)
yoyWHITE = (248,236,253)
yoyPURPLE = (215, 47, 230)
# FANCY
fSKYBLUE = (32,208,223)
fYELLOW = (250,233,119)
fWHITE = (233,233,226)
fPINK = (233,65,138)
fWHITE = (245,242,247)
# BREAKTHROUGH
bDARKBLUE = (1,13,37)
bPURPLE = (249,38,189)
bPINK = (189,17,106)
bWHITE = (248, 227, 196)
# Feel Special
fsLIGHTGOLD = (213,190,152)
fsGOLD = (186,161,120)
fsPEACH = (239,239,237)
# More and More
mamGREEN = (11,68,62)
mamGOLD = (243,171,86)
mamORANGE = (189, 72, 17)
mamWHITE = (250,234,203)


