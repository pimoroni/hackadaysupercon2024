import time
from mantabot import MantaBot

"""
A demonstration of MantaBot performing a sequence of driving movements.

Press "BOOT" to exit the program.
"""

# Constants
TIME_FOR_EACH_MOVE = 2      # The time to travel between each value
DRIVING_SPEED = 1.0         # The speed of the wheels when driving forward or backward, from 0.0 to 1.0
TURNING_SPEED = 0.2         # The speed of the wheels when turning left or right, from 0.0 to 1.0

# Variables
bot = MantaBot()    # Create a new MantaBot object
sequence = 0        # The current part of the sequence being driven

# Helper functions for driving in common directions
def drive_forward(speed):
    global bot
    bot.servo_a.value(-speed)
    bot.servo_b.value(speed)
    
def drive_backward(speed):
    global bot
    bot.servo_a.value(speed)
    bot.servo_b.value(-speed)

def turn_left(speed):
    global bot
    bot.servo_a.value(-speed)
    bot.servo_b.value(-speed)
    
def turn_right(speed):
    global bot
    bot.servo_a.value(speed)
    bot.servo_b.value(speed)

def stop():
    global bot
    bot.servo_a.value(0)
    bot.servo_b.value(0)


# Enable the servos to get started
for s in bot.servos:
    s.enable()

# Set the onboard LED to green
bot.led.set_rgb(0, 255, 0)

# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    # Continually drive the servos until "BOOT" is pressed
    while not bot.boot_pressed():

        # Set the motor speeds, based on the sequence
        if sequence == 0:
            drive_forward(DRIVING_SPEED)
        elif sequence == 1:
            drive_backward(DRIVING_SPEED)
        elif sequence == 2:
            turn_right(TURNING_SPEED)
        elif sequence == 3:
            turn_left(TURNING_SPEED)
        elif sequence == 4:
            stop()
            
        # Move on to the next part of the sequence
        sequence += 1

        # Loop the sequence back around
        if sequence >= 5:
            sequence = 0

        time.sleep(TIME_FOR_EACH_MOVE)

# Stop the servos and LED
finally:
    bot.reset()
