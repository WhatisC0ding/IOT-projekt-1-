# Importere library til at forbinde til adafruit.io
import umqtt_robust2
from machine import Pin, ADC
import GPSfunk
from hydrering import jord # Modul "hydrering", funktion "jord" for jordfugtighedssensoren
from fugtighed import humidity # Modul "fugtighed", funktion "humidity" for DHT11 luftfugtighedssensoren
from temperatur import temperature # Modul "temperatur", funktion "temperature" for DHT11 temperatursensoren
from knap import tryk # Modul "knap", "tryk" for taktil knap
import LED2 # Modul "LED2" for neopixel LED ring
import neopixel 
import dht
from time import sleep_ms, sleep, ticks_ms
lib = umqtt_robust2

# GPS Pin 16
sensor = dht.DHT11(Pin(14))
sens = ADC(Pin(36))


tempfeed = bytes('{:s}/feeds/{:s}'.format(b'DannyLy', b'tempfeed/csv'), 'utf-8')
airhumfeed = bytes('{:s}/feeds/{:s}'.format(b'DannyLy', b'airhumfeed/csv'), 'utf-8')
humfeed = bytes('{:s}/feeds/{:s}'.format(b'DannyLy', b'humfeed/csv'), 'utf-8')
# opret en ny feed kaldet map_gps indo på io.adafruit
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'DannyLy', b'mapfeed/csv'), 'utf-8')
# opret en ny feed kaldet speed_gps indo på io.adafruit
speedFeed = bytes('{:s}/feeds/{:s}'.format(b'DannyLy', b'speedfeed/csv'), 'utf-8')

prev_time = 0
interval = 20000
state = 0

timerSet = False
LED_interval = 5000
timer = 0

while True:
    current_time = ticks_ms()
    sleep_ms(500)
    knapVal = lib.knapVal
    # haandtere fejl i forbindelsen og hvor ofte den skal forbinde igen
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            # hvis der forbindes returnere is_conn_issue metoden ingen fejlmeddelse
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        #if  tryk() == 0:
            #lib.c.publish(topic=buzzer_pub, msg=str(0))
        if (current_time - prev_time > interval):
            lib.c.publish(topic=mapFeed, msg=GPSfunk.main())
            speed = GPSfunk.main()
            speed = speed[:4]
            print("speed: ",speed)
            lib.c.publish(topic=speedFeed, msg=speed)
            lib.c.publish(topic=humfeed, msg=str(jord()))
            prev_time = current_time
            lib.c.publish(topic=airhumfeed, msg=str(humidity()))
            prev_time = current_time   
            lib.c.publish(topic=tempfeed, msg=str(temperature()))
            prev_time = current_time
            print("timer conditions", temperature(), humidity(), jord())
        if temperature() > 20 and humidity() > 35 and jord() > 1:
            print("triple condition True")
            if not timerSet: 
                timer = current_time # Sætter timeren til currentTime når værdien fra jord er over 0.5V
                timerSet = True 
                print("timerSet")             
        if temperature() < 20 or humidity() < 35 or jord() < 1: 
            print("one condition False")
            timer = current_time
            if timerSet:
                timerSet = False # Stopper timeren når værdien fra jord er under 0.5V
                print("timerstop") 
        if (current_time - timer > LED_interval): # Eksekvere koden hvis (currentTime - timeren) der er blevet opdateret til er større end (intervallet) vi har sat
            while True:
                for i in range(0, 31):
                    LED2.set_color(255, 0, 0)
                    sleep(1)
                    LED2.set_color(0, 0, 0)
                    sleep(1)
                    i = i+1
                sleep(100000)
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        lib.client.disconnect()
        lib.sys.exit()
    except OSError as e:
        print('Failed to read sensor.')
    lib.c.check_msg() # needed when publish(qos=1), ping(), subscribe()
    lib.c.send_queue()  # needed when using the caching capabilities for unsent messages
lib.c.disconnect()


