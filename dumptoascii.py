import numpy as np
import subprocess
from PIL import ImageGrab, Image
import time
import os
import Xlib
from Xlib.display import Display

# Define the ASCII characters to use for the image
ascii_chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))

# Connect to the X server
display = Display()

# Get the root window
root = display.screen().root

# Get the width and height of the root window
width = root.get_geometry().width
height = root.get_geometry().height

# Use xclip to copy the contents of the root window to the clipboard
subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', '/dev/null'])

# Wait for the clipboard to be updated
time.sleep(0.5)

# Get an image from the clipboard
im = ImageGrab.grabclipboard()

# Convert the image to a grayscale numpy array
data = np.array(im)
gray = (0.2126 * data[:,:,0] + 0.7152 * data[:,:,1] + 0.0722 * data[:,:,2]).astype(np.uint8)

# Convert the grayscale image to ASCII art
ascii_image = ascii_chars[(gray * (ascii_chars.size - 1) / 255).astype(int)]

# Print the ASCII art image
print('\n'.join([''.join(row) for row in ascii_image]))

# Close the display
display.close()
