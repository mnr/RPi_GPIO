import wiringpi
from time import sleep

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(18,2) #bcm pin 18 is hardware pwm0

for j in range(3):
    for i in range(0,1024):
        wiringpi.pwmWrite(18,i)
        sleep(.001)

    for i in range(1024,0,-1):
        wiringpi.pwmWrite(18,i)
        print(i)
        sleep(.001)


# cleanup the gpio
wiringpi.digitalWrite(18,0)
wiringpi.pinMode(18,0)
