import RPi.GPIO as GPIO

pu_pin = 18
pd_pin = 23
default_up_pin = 6
default_down_pin = 24

GPIO.setmode(GPIO.BCM) # set numbering scheme
GPIO.setup(pu_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pd_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(default_up_pin, GPIO.IN) # GPIO 0-8 default to pull-up
GPIO.setup(default_down_pin, GPIO.IN) # GPIO 9-27 default to pull-down

pu_state = 0
pd_state = 0
default_up_state = 0
default_down_state = 0

looptimes = 10000
for loop in range(looptimes):
    pu_state = pu_state + GPIO.input(pu_pin)
    pd_state = pd_state + GPIO.input(pd_pin)
    default_up_state = default_up_state + GPIO.input(default_up_pin)
    default_down_state = default_down_state + GPIO.input(default_down_pin)
    
print ("average pull up value is " + str(pu_state/looptimes))
print ("average pull down value is " + str(pd_state/looptimes))
print ("average default up value is " + str(default_up_state/looptimes))
print ("average default down value is " + str(default_down_state/looptimes))
