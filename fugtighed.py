from machine import Pin
import dht
from time import sleep_ms, sleep            

sensor = dht.DHT11(Pin(14))   
  
def humidity():
    sleep(1)
    sensor.measure()
    hum = sensor.humidity()
    print("fugtigheden er:" +str(hum) +"%")
    return hum