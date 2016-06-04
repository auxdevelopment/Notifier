"""
Desc: Easy application for sending notifications
Author: Benjamin Auinger (github.com/traceur99100)

Usage: 
    python3 main.py <msg> <duration>

    msg:        message that will be shown
    duration:   defines how long the notification is visible

ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
"""

### imports ###

from tkinter import *
import sys 
import time
import re

### functions ###


"""
function:   configFileValid()
@desc:      checks if the config file has any errors
@param:     content     -   content of the config file
"""
def configFileValid(content):
    attributes = "(width|height|background-color|font|font-size|font-color|coords)"
    attributeList = content.split("\n")
    attributeListNew = []    

    # remove all comments
    for attribute in attributeList:
        if(not(attribute.startswith("#") or attribute.startswith("\n") or attribute == "")):
            attributeListNew.append(attribute)

    for attribute in attributeListNew:
        if not (re.search("%s=[a-zA-Z0-9 ]+#?(.+)?" %(attributes), attribute)):
            return False
    return True


"""
function:   getAttribute(attribute)
@desc:      returns a specific attribute from the config file, 
            if it doesnt exist an exception will be risen

@param:
            attribute   -   defines the attribute which will be returned from
                            the config file
"""
def getAttribute(attribute):
    content = ""
    with open("notifierrc", "r") as configFile:
        content = configFile.read()

    # raise an exception if the config file isnt valid
    if(not configFileValid(content)):
        raise ValueError("Config files contains syntax errors")

    contentList = content.split("\n")

    for line in contentList:
        if(line.startswith(attribute)):
            return line


"""
function:   getWidth()
@desc:      returns the defined width in the config file
"""
def getWidth():
    width = getAttribute("width")
    if(re.match("width=[0-9]+", width)):
        return int(width.split("=")[1])
    raise ValueError("width: invalid value")


"""
function:   getHeight()
@desc:      returns the defined height in the config file
"""
def getHeight():
    height = getAttribute("height")
    if(re.match("height=[0-9]+", height)):
        return int(height.split("=")[1])
    raise ValueError("height: invalid value")

"""
function:   getCoords()
@desc:      returns a tupple containing x and y coords
"""
def getCoords():
    coords = getAttribute("coords")
    if(re.match("coords=([0-9]+\s[0-9]+|top-left|top-right|bottom-right|bottom-left)", coords)):
        coords = coords.split("=")[1]
        
        if(coords == "top-right"):
            pass
        elif(coords == "top-left"):
            pass
        elif(coords == "bottom-right"):
            pass
        elif(coords == "bottom-left"):
            pass

        coords = coords.split(" ")
        return (int(coords[0]), int(coords[1]))
    raise ValueError("coords: invalid value")


"""
function:   getFont()
@desc:      return the font defined in the config file
"""
def getFont():
    font = getAttribute("font")
    if(re.match("font=[a-zA-Z_-]+")):
        return font.split("=")[1]
    raise ValueError("font: invalid value")


"""
function:   getFontSize()
@desc:      returns the font size defined in the config file
"""
def getFontSize():
    font_size = getAttribute("font-size")
    if(re.match("font-size=[0-9]+")):
        return font_size.split("=")[1]
    raise ValueError("font-size: invalid value")


"""
function:   getBackgroundColor()
@desc:      returns background-color attribute
"""
def getBackgroundColor():
    background_color = getAttribute("background-color")
    if(re.match("background-color=[0-9a-fA-F]{3,6}", background_color)):
        return background_color.split("=")[1]
    raise ValueError("background-color: invalid value")


"""
function:   getFontColor()
@desc:      returns font-color attribute
"""
def getFontColor():
    font_color = getAttribute("font-color")
    if(re.match("font-color=[0-9a-fA-F]{3,6}", font_color)):
        return font_color.split("=")[1]
    raise ValueError("font-color: invalid value")


"""
function:   sendMessage(msg, duration)
@desc:      creates a window with a message, position and size are defined by the config file
@param:
            msg         -   message that will be shown
            duration    -   defines how long the notification is visible
"""
def sendMessage(msg, duration):
    window = Tk()
    canvas = Canvas(window, width=getWidth(), height=getHeight())
    canvas.pack()
    
    canvas.create_rectangle((0,0,getWidth(), getHeight()), fill="#" + getBackgroundColor())
    canvas.create_text((getWidth() // 2, getHeight() // 2), text=msg, fill="#" + getFontColor(), font=(getFont(), getFontSize()))
    
    window.overrideredirect(1) 
    window.after(duration, lambda: window.destroy())
    window.title(string="Notification")
    window.resizable(width=False,height=False)
    window.geometry('%dx%d+%d+%d' % (getWidth(), getHeight(), getCoords()[0], getCoords()[1]))
    
    
    window.mainloop()

if __name__ == "__main__":
    msg = sys.argv[1]
    duration = sys.argv[2]
    sendMessage(msg, duration)
