import time
import math
from mantabot import MantaBot

"""
Demonstrates how to create a Servo object and control it.
"""

# Constants
SLEEP = 2           # The time to sleep (in seconds) between the main movements
SWEEPS = 3          # How many sinewave sweeps of the servo to perform
SWEEP_EXTENT = 1.0  # How far from zero to drive the servo when sweeping
SWEEP_SLEEP = 0.02  # The time to sleep (in seconds) between the each sweep update

# Variables
bot = MantaBot()    # Create a new MantaBot object
s = bot.servo_a     # Access the servo we want to control (either servo_a or servo_b)

# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    # Enable the servo (this puts it at zero speed)
    s.enable()
    time.sleep(SLEEP)

    # Go to min
    s.to_min()      # Shorthand for s.value(-1.0)
    time.sleep(SLEEP)

    # Go to max
    s.to_max()      # Shorthand for s.value(1.0)
    time.sleep(SLEEP)

    # Go back to mid
    s.to_mid()      # Shorthand for s.value(0.0)
    time.sleep(SLEEP)

    # Do a sine sweep
    for j in range(SWEEPS):
        for i in range(360):
            s.value(math.sin(math.radians(i)) * SWEEP_EXTENT)
            time.sleep(SWEEP_SLEEP)

# Stop the servos and LED
finally:
    bot.reset()
