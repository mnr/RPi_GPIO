import gpiozero as gpzero
from time import sleep

resetbutton = gpzero.Button(3)
leds = gpzero.LEDBoard(26,16,20,21)

#  test the button
while True:
    if resetbutton.is_pressed:
        print("Great! The button is correctly connected")
        break
    else:
        print("Please test the pushbutton now...")

# test the leds
leds.on()    
sleep(3)
leds.value = (0,0,0,1)
sleep(1)
leds.value = (0,0,1,0)
sleep(1)
leds.value = (0,1,0,0)
sleep(1)
leds.value = (1,0,0,0)
sleep(1)
leds.off()
