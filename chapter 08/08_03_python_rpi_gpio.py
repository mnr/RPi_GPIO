# example of programming Raspberry Pi GPIO with rpi.gpio
# refer to sourceforge.net/p/raspberry-gpio-python/wiki/Home

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM) # declare BCM numbering scheme (vs GPIO.BOARD)

# set up pushbutton and bank of leds
resetbutton = 3
leds = [26, 16, 20, 21]
GPIO.setup(3, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

# function to handle reset button
def handleReset ():
    while not GPIO.input(resetbutton):
        GPIO.output(leds, GPIO.HIGH)
        print("waiting for button")
    resetLightsandCounter()


def resetLightsandCounter():
    global counter
    GPIO.output(leds, GPIO.LOW)
    counter = 0
    print("reset")
    
    
# setup button handlers
GPIO.add_event_detect(resetbutton, GPIO.FALLING)

# send 0...15 to lights
while True:
    resetLightsandCounter()
    while counter < 16:
        if GPIO.event_detected(resetbutton):
            handleReset()
        GPIO.output(leds, (
            GPIO.HIGH if counter & 0b1000 else GPIO.LOW,
            GPIO.HIGH if counter & 0b0100 else GPIO.LOW,
            GPIO.HIGH if counter & 0b0010 else GPIO.LOW,
            GPIO.HIGH if counter & 0b0001 else GPIO.LOW
        )
    )
        counter += 1
        sleep(1)
#    
    