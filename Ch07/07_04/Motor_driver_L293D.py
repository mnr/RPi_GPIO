import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

MotorForward = 16      # GPIO.BOARD pin 16
MotorBackward = 18     # GPIO.BOARD pin 18
MotorEnable = 22       # GPIO.BOARD pin 22

GPIO.setup(MotorForward,GPIO.OUT)
GPIO.setup(MotorBackward,GPIO.OUT)
GPIO.setup(MotorEnable,GPIO.OUT)

for i in range(3):
    print ("Turning Forward")
    GPIO.output(MotorForward,GPIO.HIGH)
    GPIO.output(MotorBackward,GPIO.LOW)
    GPIO.output(MotorEnable,GPIO.HIGH)

    time.sleep(1)

    print ("Turning Backwards")
    GPIO.output(MotorForward,GPIO.LOW)
    GPIO.output(MotorBackward,GPIO.HIGH)
    GPIO.output(MotorEnable,GPIO.HIGH)

    time.sleep(1)

    print ("Motor Stop")
    GPIO.output(MotorEnable,GPIO.LOW)

    time.sleep(1)

GPIO.cleanup()
