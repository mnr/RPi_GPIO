import wiringpi
from time import sleep

wiringpi.wiringPiSetupGpio()

# bcm pin 18 is hardware pwm0
# 2nd argument: input = 0, output=1, PWM=2
wiringpi.pinMode(18,2) 

try:
    for j in range(200):
        for i in range(0,1024):
            wiringpi.pwmWrite(18,i)
            sleep(.001)

        for i in range(1024,0,-1):
            wiringpi.pwmWrite(18,i)
            print(i)
            sleep(.001)
except KeyboardInterrupt: #control-c
    # cleanup the gpio
    wiringpi.digitalWrite(18,0)
    wiringpi.pinMode(18,0)



