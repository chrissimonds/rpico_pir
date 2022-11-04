# This program is using the Raspberry Pi Pico to gather data using a simple PIR sensor
# This program was written so as it could be used with either Pico or Pico W
# This was written using MicroPython version 1.19.1 

import rp2
import machine
from machine import Pin
import utime
import time
from time import sleep
import sys

# Print the Raspberry Pi Pico system information:
#   Welcome, here is the system info:
#   (name='micropython', version=(1, 19, 1), _machine='Raspberry Pi Pico with RP2040', _mpy=4358)

print('Welcome, here is the system info:')
print (str(sys.implementation))
print()

# Timestamp class RTC will set time correctly when using Thonny and connected to a computer and manually initiated
# otherwise clock will init to the wrong value of 2021-01-01 00:00:01
rtc=machine.RTC()
timestamp=rtc.datetime()
timestring="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7])

print ('Date and Time = ' + timestring)


#The program will use a logging file called data.txt which will need to be created before executing this code
# You can create the file the first time from the command line with the following
  # file = open("data.txt","w")
  # file.close()
# Please repeat commands above from command prompt to reset and empty file

file = open("data.txt")
file.read()
file.write(timestring + ",Sys Info: " + str(sys.implementation) + "\n")
file.close()


# Read and print the CPU temperature 
# sensor_temp = machine.ADC(4)

sensor_temp = machine.ADC(machine.ADC.CORE_TEMP)
conversion_factor = 3.3 / (65535)
reading = sensor_temp.read_u16() * conversion_factor
temperature = 27 - (reading - 0.706)/0.001721
fahrenheit= temperature * (9 / 5) + 32
print('Temperature = ' + str(temperature) + ' C  ' + str(fahrenheit) + ' F')


# Onboard LED Setup
# This is the new and preferred method that works with both Pico and Pico W models
led = machine.Pin("LED", machine.Pin.OUT)
led.off()

# For the PIR sensor please remove jumper for best performance
# Also dials may need to be adjusted but should not be
# Experiment as needed with the PIR jumper settings and the sensitivy for desired motion triggering
# Connect GP16 to PIR sensor's OUT pin), please use 3.3V connect to VCC on PIR sensor and GND to GND
# Please remove the plastic shield to see the pin labels.
# Connect the Pico's GP16 to PIR sensor's OUT pin.
# Connect the Pico's 3.3V Pin to PIR sensor's OUT pin.
# Connect the Pico's GND pin to PIR sensor's GND pin.

pir = Pin(16, Pin.IN, Pin.PULL_UP)


# Main program loop to run sensor and write info to data.txt
while True:
    file = open("data.txt")
    file.read()
    file.write(timestring + ", Temp " + str(temperature) + ' C  ' + str(fahrenheit) + ' F' + "\n")
    file.write(timestring + ", PIR  " + str(pir.value()) + "\n")
#    file.flush()
    file.close()
    sleep(1)
    print(pir.value())   
    if pir.value() != 0:
        print('Motion Detected and Temperature is ' + str(temperature) + ' C  ' + str(fahrenheit) + ' F') 
        led.on()
    else:
        print('Waiting for movement and Temperature is ' + str(temperature) + ' C  ' + str(fahrenheit) + ' F') 
        led.off()
