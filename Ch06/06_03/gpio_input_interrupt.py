import RPi.GPIO as GPIO
import atexit
import time

def exit_handler():
    GPIO.cleanup()

atexit.register(exit_handler)

def my_callback(channel):
    print("The switch changed")

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(4,GPIO.RISING,callback=my_callback)

while True:
    # here's where your code does something while it waits
    time.sleep(3)
    print("waiting...")
    


