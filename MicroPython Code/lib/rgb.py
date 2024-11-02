# SPDX-FileCopyrightText: 2024 Christopher Parrott for Pimoroni Ltd
#
# SPDX-License-Identifier: MIT

from machine import Pin, PWM


def rgb_from_hsv(h, s, v):
    if s == 0.0:
        return v, v, v
    else:
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p, q, t = v * (1.0 - s), v * (1.0 - s * f), v * (1.0 - s * (1.0 - f))

        i = i % 6
        if i == 0:
            return v, t, p
        elif i == 1:
            return q, v, p
        elif i == 2:
            return p, v, t
        elif i == 3:
            return p, q, v
        elif i == 4:
            return t, p, v
        elif i == 5:
            return v, p, q


# A basic wrapper for PWM with regular on/off and toggle functions from Pin
# Intended to be used for driving LEDs with brightness control & compatibility with Pin
class PWMLED:
    def __init__(self, pin, invert=False, gamma=1):
        self.__gamma = gamma
        self.__led = PWM(Pin(pin), freq=1000, duty_u16=0, invert=invert)

    def brightness(self, brightness):
        self.__brightness = min(1.0, max(0.0, brightness))
        self.__led.duty_u16(int(pow(self.__brightness, self.__gamma) * 65535 + 0.5))

    def on(self):
        self.brightness(1)

    def off(self):
        self.brightness(0)

    def toggle(self):
        self.brightness(1 - self.__brightness)


class RGBLED:
    def __init__(self, r, g, b, invert=True, gamma=1):
        self.led_r = r if isinstance(r, PWMLED) else PWMLED(r, invert=invert, gamma=gamma)
        self.led_g = g if isinstance(g, PWMLED) else PWMLED(g, invert=invert, gamma=gamma)
        self.led_b = b if isinstance(b, PWMLED) else PWMLED(b, invert=invert, gamma=gamma)

    def __rgb(self, r, g, b):
        self.led_r.brightness(r)
        self.led_g.brightness(g)
        self.led_b.brightness(b)

    def set_rgb(self, r, g, b):
        self.__rgb(r / 255, g / 255, b / 255)

    def set_hsv(self, h, s, v):
        self.__rgb(*rgb_from_hsv(h, s, v))
