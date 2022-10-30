import rp2
import machine
from machine import Pin
import utime
import time
from time import sleep
import sys


print('Welcome, here is the system info:')
print (str(sys.implementation))
print()

# Timestamp class RTC will set time correctly when using Thonny
# otherwise clock will init wrong value
rtc=machine.RTC()
timestamp=rtc.datetime()
timestring="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7])

print ('Date and Time = ' + timestring)

# Read and print the CPU temperature 
# sensor_temp = machine.ADC(4)
sensor_temp = machine.ADC(machine.ADC.CORE_TEMP)
conversion_factor = 3.3 / (65535)
reading = sensor_temp.read_u16() * conversion_factor
temperature = 27 - (reading - 0.706)/0.001721
fahrenheit= temperature * (9 / 5) + 32
print('Temperature = ' + str(temperature) + ' C  ' + str(fahrenheit) + ' F')


# Onboard LED Setup
led = machine.Pin("LED", machine.Pin.OUT)
led.off()


# For the PIR sensor please remove jumper for best performance
# Also dials may need to be adjusted but should not be
# Connect GP16 to PIR sensor's OUT pin), please use 3.3V connect to VCC on PIR sensor and GND to GND
pir = Pin(16, Pin.IN, Pin.PULL_UP)
print(pir.value())

while True:
    led.off()
    # please create a new file the first time from the command line with the following
    # file = open("data.txt","w")
    # file.close()
    # Please repeat commands above from command prompt to reset and empty file
    file = open("data.txt")
    file.read()
    file.write(timestring + ", Temp " + str(temperature) + "\n")
    file.write(timestring + ", PIR  " + str(pir.value()) + "\n")
    file.flush()
    file.close()
    print(pir.value())   
    if pir.value() != 0:
        print('Motion Detected')
        led.on()
        sleep(0.1)
    else:
        print('waiting for movement')
        led.off()
        sleep(0.1)
