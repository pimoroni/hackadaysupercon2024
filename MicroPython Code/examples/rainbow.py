import time
from mantabot import MantaBot

"""
How to have MantaBot's onboard RGB LED cycle through the rainbow.

Press "BOOT" to exit the program.
"""

# Constants
SATURATION = 1.0    # The colour's saturation (from 0.0 to 1.0)
VALUE = 1.0         # The colour's value/brightness (from 0.0 to 1.0)
SPEED = 0.01        # The speed that the LED will cycle its colour at
UPDATES = 60        # How many times the LED will be updated per second
UPDATE_RATE = 1 / UPDATES

# Variables
bot = MantaBot()    # Create a new MantaBot object
hue = 0             # The hue that will change over time

# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    # Continually cycle the RGB LED until "BOOT" is pressed
    while not bot.boot_pressed():
        
        # Set MantaBot's onboard RGB LED to the colour
        bot.led.set_hsv(hue, SATURATION, VALUE)
        
        # Advance the hue by the speed, wrapping back to 0.0 if it reaches 1.0
        hue = (hue + SPEED) % 1.0
        
        time.sleep(UPDATE_RATE)
    
# Stop the servos and LED
finally:
    bot.reset()