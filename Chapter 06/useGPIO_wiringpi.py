import wiringpi as wirePi

# References pins by wiringpi scheme
inputPin = 7
wirePi.wiringPiSetup()

### References pins by physical location
##inputPin = 7
##wirePi.wiringPiSetupPhys()

### References pins by BCM
##inputPin = 4
##wirePi.wiringPiSetupGpio()

# define inputPin as looking for input
wirePi.pinMode(inputPin,0)

# set the pulldown resistor on the pin
wirePi.pullUpDnControl(inputPin,wirePi.PUD_DOWN)

while True:
    # read pin using board numbering system
    
    if wirePi.digitalRead(inputPin):
        print ("Switch Closed") #happens if switch is closed
    else:
        print ("Switch Open") #happens if switch is open

