import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(4):
        print ("Switch is closed")
    else:
        print ("Switch is open")

GPIO.cleanup()
        
