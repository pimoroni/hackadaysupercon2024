import time
from mantabot import MantaBot
from breakout_ltr559 import BreakoutLTR559

"""
A demonstration of MantaBot driving towards an object that gets near it.

Press "BOOT" to exit the program.
"""

# Constants
UPDATES = 50                    # How many times to update the servos per second
UPDATE_RATE = 1 / UPDATES
MAX_PROX = 120                   # The maximum proximity value to respond to

# Variables
bot = MantaBot()                # Create a new MantaBot object
ltr = BreakoutLTR559(bot.i2c)   # Create a new LTR559 object using MantaBot's I2C bus

# Enable the servos to get started
for s in bot.servos:
    s.enable()

# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    # Continually drive the servos until "BOOT" is pressed
    while not bot.boot_pressed():

        # Read the sensor
        reading = ltr.get_reading()
        
        if reading is not None:
            # Scale the proximity to be a servo speed
            speed = reading[BreakoutLTR559.PROXIMITY] / MAX_PROX
                
            # Apply the speed to the servos
            bot.servo_b.value(speed)
            bot.servo_a.value(-speed)

        time.sleep(UPDATE_RATE)

# Stop the servos and LED
finally:
    bot.reset()
