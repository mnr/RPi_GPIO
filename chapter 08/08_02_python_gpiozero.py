# example of programming Raspberry Pi GPIO with gpiozero
# refer to gpiozero.readthedocs.io

import gpiozero as gpzero
from time import sleep

# set up pushbutton and bank of leds
resetbutton = gpzero.Button(3)
leds = gpzero.LEDBoard(26,16,20,21)

# functions to control behavior
def LightsOn ():
    while resetbutton.is_pressed:
        leds.on()
    
def ResetCounter ():
    global counter
    leds.off()
    counter = 0
    
def binary2lights(showThis):
    leds.value = (
        showThis & 0b1000,
        showThis & 0b0100,
        showThis & 0b0010,
        showThis & 0b0001)
    
# setup button handlers    
resetbutton.when_pressed = LightsOn
resetbutton.when_released = ResetCounter

# send 0...15 to lights
while True:
    ResetCounter()
    while counter < 16:
        binary2lights(counter)
        counter += 1
        sleep(1)
    
    