import wiringpi
from time import sleep

MotorForward = 16
MotorBackward = 22
MotorEnable = 18

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(MotorEnable,2) #bcm pin 18 is hardware pwm0
wiringpi.pinMode(MotorForward,1)
wiringpi.pinMode(MotorForward,1)
wiringpi.pinMode(MotorBackward,1)

def function PwmControl(self,turnForward):
    if turnForward:
        for i in range(255):
            wiringpi.pwmWrite(MotorEnable,i)
            sleep(.001)
    else:
        for i in range(255,0,-1):
            wiringpi.pwmWrite(MotorEnable,i)
            sleep(.001)

try:
    for j in range(3):
        print ("Turning Forward")
        wiringpi.digitalWrite(MotorForward,1)
        wiringpi.digitalWrite(MotorBackward,0)
        PwmControl(True)
        PwmControl(False)
            
        print ("Turning Backwards")
        wiringpi.digitalWrite(MotorForward,0)
        wiringpi.digitalWrite(MotorBackward,1)
        PwmControl(True)
        PwmControl(False)
except KeyboardInterrupt: #control-c
    # cleanup the gpio
    wiringpi.digitalWrite(MotorForward,0)
    wiringpi.digitalWrite(MotorBackward,0)
    wiringpi.pwmWrite(MotorEnable,0)
