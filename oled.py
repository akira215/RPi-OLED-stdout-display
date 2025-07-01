# Akira215Corp

# This script shall be started at the boot of the RPI
# it will monitor 2 RAM files (defined in fname_line1 & 2)
# and display their content @ $pollinterval
# If either of 1 line content is 'cls', screen will be
# cleared.
# A screensaver is triggered if $screensaver_delay is overpasss
# without any changes in 'line1' and 'line2' files

import os
import time
import subprocess
from math import *
from pathlib import Path

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# --- Config -------------------------
# pollinterval in second for refreshing
pollinterval = 0.2
# delay in second before cls
screensaver_delay = 120
fname_line1 = "/tmp/oled-display/line1" 
fname_line2 = "/tmp/oled-display/line2" 
# --- Config -------------------------



def SecondsToHms(seconds):
    mm, ss = divmod(seconds, 60)
    # Get hours
    hh, mm= divmod(mm, 60)

    return "-> " + str(hh) + "h " + str(mm) + "m " + str(ss) + "s"


def readline_in_file(fname):
    line = ""
    try:
        f = open(fname, 'r')
    except FileNotFoundError:
        if readline_in_file.showErr:
            print(f"oled.py: File {fname} not found.  Aborting")
            readline_in_file.showErr = False
    except OSError:
        if readline_in_file.showErr:
            print(f"oled.py: OS error occurred trying to open {fname}")
            readline_in_file.showErr = False
    except Exception as err:
        if readline_in_file.showErr:
            print(f"oled.py: Unexpected error opening {fname} is",repr(err))
            readline_in_file.showErr = False
    else:
        with f:
            readline_in_file.showErr = True
            line = f.readline().rstrip()
            f.close()
    
    return line

readline_in_file.showErr = True

# create the file and the corresponding folders

if not Path(fname_line1).exists():
    Path(fname_line1).parent.mkdir(parents=True, exist_ok=True)
    with open(fname_line1, 'w') as f:
        f.write("")
    os.chmod(fname_line1, 0o666)

if not Path(fname_line2).exists():
    Path(fname_line2).parent.mkdir(parents=True, exist_ok=True)
    with open(fname_line2, 'w') as f:
        f.write("")
    os.chmod(fname_line2, 0o666)

# setup counters
counter_wo_changes = ceil(screensaver_delay / pollinterval)
counter = counter_wo_changes

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)

#file = open('/dev/shm/output', 'r')
l1 = ""
l2 = ""

timer = False
start = time.time()

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # backup values
    old_l1 = l1
    old_l2 = l2

    # Safelty read the RAM files
    l1 = readline_in_file(fname_line1)
    l2 = readline_in_file(fname_line2)

    # Process timer
    if l2 == "timer":
        timer = True
        start = time.time()
    elif not l2.startswith("-> "):
        timer = False

    if timer:
        with open(fname_line2, "w") as f:
            f.write(SecondsToHms(floor(time.time()-start)))
            #f.write("-> " + str(floor(time.time()-start)))


    # Catch clear screen
    if l1 == "cls" or l2 == "cls":
        print(f"oled.py: cls required by input")
        display1 = ""
        display2 = ""
    else:
        display1 = l1
        display2 = l2
    
    # Check if we have to go to screen saving
    if l1 == old_l1 and l2 == old_l2:
        counter -= 1
        if counter <= 0:
            if counter == 0:
                print(f"oled.py: no updated datas since {screensaver_delay}s. Triggering screensaving")
            counter = -1
            display1 = ""
            display2 = ""
    else:
        counter = counter_wo_changes


    # Write 2 lines of text.
    draw.text((x, top),  display1 , font=font, fill=255)
    draw.text((x, top+16),  display2,  font=font, fill=255)


    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(pollinterval)