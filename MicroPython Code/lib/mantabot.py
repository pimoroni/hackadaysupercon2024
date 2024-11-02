# SPDX-FileCopyrightText: 2024 Christopher Parrott for Pimoroni Ltd
#
# SPDX-License-Identifier: MIT

from machine import Pin
from pimoroni_i2c import PimoroniI2C
from rgb import RGBLED
from servo import Servo, CONTINUOUS

NUM_SERVOS = const(2)
NUM_ADCS = const(3)


class MantaBot:
    SPICE_TX_PIN = 8
    SPICE_RX_PIN = 9
    SPICE_NETLIGHT_PIN = 10
    SPICE_RESET_PIN = 11
    SPICE_PWRKEY_PIN = 7

    I2C_SDA_PIN = 12
    I2C_SCL_PIN = 13

    RGB_PINS = (18, 19, 20)

    SERVO_PINS = (21, 22)

    USER_SW_PIN = 23

    SENSOR_PIN = 26

    ADC1_PIN = 27
    ADC2_PIN = 28
    ADC3_PIN = 29

    RGB_GAMMA = 1.0

    def __init__(self, init_i2c=True):
        # Set up the i2c for Qw/st, if the user wants
        if init_i2c:
            self.i2c = PimoroniI2C(self.I2C_SDA_PIN, self.I2C_SCL_PIN, 100000)

        # Set up the RGB LED
        self.led = RGBLED(*self.RGB_PINS, invert=True, gamma=self.RGB_GAMMA)
        
        # Set up the two servos
        self.servos = [Servo(s, CONTINUOUS) for s in self.SERVO_PINS]
        
        # Currently the blue LED component is on the same PWM slice as Servo A, so we need to set the colour once the servos are initialised
        self.led.set_rgb(0, 0, 0)

        # Set up the user switch
        self.__switch = Pin(self.USER_SW_PIN, Pin.IN, Pin.PULL_UP)

    def boot_pressed(self):
        return self.__switch.value() == 0

    @property
    def servo_a(self):
        return self.servos[0]

    @property
    def servo_b(self):
        return self.servos[1]
    
    def reset(self):
        self.servos[0].disable()
        self.servos[1].disable()
        self.led.set_rgb(0, 0, 0)
