# read the ds18b20 one-wire temperature sensor
# 

import RPi.GPIO as GPIO
import os
import re

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# output pwm via GPIO 26 (pin 37)
GPIO.setup(26, GPIO.OUT)
pwmToMeter = GPIO.PWM(26, 50) # GPIO26, 50Hz
pwmToMeter.start(0) # start PWM with duty cycle = 0

# helper functions
def getTemps():
    # returns a list of temperatures from all available "28*" onewire devices
    allTemps = list()
    onewire_basedir = "/sys/bus/w1/devices/"
    onewire_devices = os.listdir(onewire_basedir)
    onewire_retemp = re.compile('t=(\d*)')
    for thistring in onewire_devices:
        if(thistring.startswith("28")):
            onewire_path = os.path.join(onewire_basedir, thistring, "w1_slave")
            onewire_devfile = open(onewire_path, "r")
            onewire_devtext = onewire_devfile.readlines()
            onewire_temp = onewire_retemp.search(onewire_devtext[1])
            allTemps.append(onewire_temp.group(1))
    return(allTemps)

# set scaling from temperature to meter
def normalRange(temperature):
    # assumes temperature is a list of values, -55000 < temp < 125000
    temp_floor = 5000 # readings below this are pegged at zero %
    temp_ceiling = 50000 # readings above this are pegged at 100%
    meterRange = 100 # pwm duty cycle is 0 to 100
    rtn_values = list()
    for atemp in temperature:
        atemp = int(atemp)
        atemp = temp_floor if atemp < temp_floor else atemp
        atemp = temp_ceiling if atemp > temp_ceiling else atemp
        rtn_values.append( int( meterRange * (atemp - temp_floor) / (temp_ceiling - temp_floor)) )
    return(rtn_values)

try:
    while True:
        all_temps = getTemps()
        #print(all_temps)
        if all_temps:
            pwm_values = normalRange(all_temps)
            #print(pwm_values)
            average_temp = sum(pwm_values) / len(pwm_values)
            pwmToMeter.ChangeDutyCycle(average_temp)
            print("Raw sensor: ", all_temps, "pwm values: ", pwm_values, "Average pwm: ", average_temp)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()