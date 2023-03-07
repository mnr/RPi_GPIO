from gpiozero import LED, Button
from signal import pause

mySwitch = Button(2)
myLED = LED(26)

# test the connections
# myLED.blink()

mySwitch.when_pressed = myLED.on
mySwitch.when_released = myLED.off

pause()


