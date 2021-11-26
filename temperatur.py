from machine import Pin
import dht
from time import sleep_ms, sleep            

sensor = dht.DHT11(Pin(14))   
  
def temperature():
    sleep(1)
    sensor.measure()
    temp = sensor.temperature()
    print("temperaturen er:" +str(temp) +"C")
    return temp