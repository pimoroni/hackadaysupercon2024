import time
from machine import Pin
from mantabot import MantaBot

"""
A demonstration of MantaBot performing a driving sequence when it detects motion.

Press "BOOT" to exit the program.
"""

# Constants
TIME_FOR_TURN = 0.6     # The time to turn for
TIME_FOR_DRIVE = 1.0    # The time to drive for
TIME_FOR_STOP = 1.0     # The time to stop, after moving
CHECK_SLEEP = 0.5       # The time to wait between each sensor check
TURNING_SPEED = 0.2     # The speed of the wheels when turning left or right, from 0.0 to 1.0
DRIVING_SPEED = 1.0     # The speed of the wheels when driving forward or backward, from 0.0 to 1.0
REPEATS = 2             # How many times to repeat the movements for


# Variables
bot = MantaBot()    # Create a new MantaBot object

# Set up a pin for reading the PIR sensor connected to MantaBot
pir = Pin(bot.SENSOR_PIN, Pin.IN, Pin.PULL_UP)
last_detection = True   # Start assuming a previous detection, in case the sensor is immediately triggered

# Helper functions for driving in common directions
def drive_forward(speed):
    global bot
    bot.servo_a.value(-speed)
    bot.servo_b.value(speed)
    
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



# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    # Continually drive the servos until "BOOT" is pressed
    while not bot.boot_pressed():

        detection = pir.value() == 1
        print("Detection:", detection)

        # Has motion been detected?
        if detection and not last_detection:
            
            # Set the onboard LED to cyan
            bot.led.set_rgb(0, 255, 255)

            for _ in range(0, REPEATS + 1):
                
                # Turn on the spot
                turn_right(TURNING_SPEED)
                time.sleep(TIME_FOR_TURN)
                
                # Drive forward
                drive_forward(DRIVING_SPEED)
                time.sleep(TIME_FOR_DRIVE)

            stop()
            time.sleep(TIME_FOR_STOP)
        else:
            # Set the onboard LED to yellow
            bot.led.set_rgb(255, 255, 0)
            
            time.sleep(CHECK_SLEEP)

        last_detection = detection

# Stop the servos and LED
finally:
    bot.reset()

