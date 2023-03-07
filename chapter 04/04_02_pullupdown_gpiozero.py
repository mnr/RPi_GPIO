from gpiozero import Button

pu_pin = Button(18, pull_up = True)
pd_pin = Button(23, pull_up = False)
default_up_pin = Button(6)
default_down_pin = Button(24)

pu_state = 0
pd_state = 0
default_up_state = 0
default_down_state = 0

looptimes = 10000
for loop in range(looptimes):
    pu_state = pu_state + pu_pin.value
    pd_state = pd_state + pd_pin.value
    default_up_state = default_up_state + default_up_pin.value
    default_down_state = default_down_state + default_down_pin.value
    
print ("average pull up value is " + str(pu_state/looptimes))
print ("average pull down value is " + str(pd_state/looptimes))
print ("average default up value is " + str(default_up_state/looptimes))
print ("average default down value is " + str(default_down_state/looptimes))

