import time
from mantabot import MantaBot
import sys
import select


"""
Control MantaBot with commands over USB serial.
    l = left
    r = right
    f = forward
    b = back

Press "BOOT" to exit the program.
"""

# Constants
TIME_FOR_EACH_MOVE = .25      # The time to travel between each value
DRIVING_SPEED = 0.25         # The speed of the wheels when driving forward or backward, from 0.0 to 1.0
TURNING_SPEED = 0.1         # The speed of the wheels when turning left or right, from 0.0 to 1.0

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

        # Poll the USB serial port for commands r,l,f,b
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:        
            ch = sys.stdin.read(1)

            if (ch == 'r'):
                turn_right(TURNING_SPEED)
                time.sleep(TIME_FOR_EACH_MOVE)
                
            if (ch == 'l'):
                turn_left(TURNING_SPEED)
                time.sleep(TIME_FOR_EACH_MOVE)
                
            if (ch == 'f'):
                drive_backward(DRIVING_SPEED)
                time.sleep(TIME_FOR_EACH_MOVE)

            if (ch == 'b'):
                drive_forward(DRIVING_SPEED)
                time.sleep(TIME_FOR_EACH_MOVE)

            stop()
            ch = ""


# Stop the servos and LED
finally:
    bot.reset()
