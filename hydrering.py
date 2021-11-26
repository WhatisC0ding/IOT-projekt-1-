from machine import Pin, ADC
from time import sleep_ms, sleep

sens = ADC(Pin(36))
#sens.atten(ADC.ATTN_11DB)
#sens.width(ADC.WIDTH_12BIT)

def jord(): 
    sleep(1)
    sens_val = sens.read()
    spaending = sens_val * (3.3 / 4096)
    print("spaending er:", spaending)
    return spaending