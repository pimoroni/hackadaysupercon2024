import time
from mantabot import MantaBot
from qwstpad import QwSTPad

"""
A demonstration of MantaBot driving under remote control

Press "BOOT" to exit the program.
"""

# Constants
UPDATES = 50                # How many times to update the servos per second
UPDATE_RATE = 1 / UPDATES
SPEED = 1.0                 # The speed of the wheels when driving or turning, from 0.0 to 1.0

# Variables
bot = MantaBot()            # Create a new MantaBot object
pad = QwSTPad(bot.i2c)      # Create a new QwSTPad object using MantaBot's I2C bus

# Enable the servos to get started
for s in bot.servos:
    s.enable()

# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    # Continually drive the servos until "BOOT" is pressed
    while not bot.boot_pressed():

        # Read all of the QwSTPad's buttons
        buttons = pad.read_buttons()
        
        # Determine the left and right speeds
        left_speed = 0
        right_speed = 0
        if buttons['U']:
            left_speed += SPEED
        
        if buttons['D']:
            left_speed -= SPEED
            
        if buttons['X']:
            right_speed += SPEED
        
        if buttons['B']:
            right_speed -= SPEED
            
        # Apply the speeds to the servos
        bot.servo_b.value(left_speed)
        bot.servo_a.value(-right_speed)

        time.sleep(UPDATE_RATE)

# Stop the servos and LED
finally:
    bot.reset()
