from machine import Pin
import neopixel
import fugtighed
from time import sleep

def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b, 128)
    np.write()

n = 12
p = 15

np = neopixel.NeoPixel(Pin(p), n)