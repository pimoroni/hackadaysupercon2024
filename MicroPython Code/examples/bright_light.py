import time
import random
from mantabot import MantaBot
from breakout_ltr559 import BreakoutLTR559

"""
A demonstration of MantaBot driving randomly when exposed to a bright light.

Press "BOOT" to exit the program.
"""

# Constants
LUX_THRESHOLD = 120             # The lux value above which MantaBot will start randomly moving
TIME_FOR_EACH_MOVE = 0.2        # The time each random movement will last

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
            # Get the brightness level
            lux = reading[BreakoutLTR559.LUX]
            print("LUX:", lux)
                
            if lux > LUX_THRESHOLD:
                # Have the robot move randomly
                bot.servo_b.value(random.uniform(-1.0, 1.0))
                bot.servo_a.value(random.uniform(-1.0, 1.0))
                bot.led.set_rgb(255, 0, 0)
            else:
                # Stop moving
                bot.servo_b.value(0)
                bot.servo_a.value(0)
                bot.led.set_rgb(0, 255, 0)

            time.sleep(TIME_FOR_EACH_MOVE)

# Stop the servos and LED
finally:
    bot.reset()
