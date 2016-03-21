import wiringpi2

pin_board = 7
pin_bcm = 4
pin_wiringpi = 7

while True:
    # read pin using board numbering system
    wiringpi2.wiringPiSetup()
    wiringpi2.pinMode(pin_board,0)
    if wiringpi2.digitalRead(pin_board):
        print ("BOARD-", end="") #happens if switch is closed
    else:
        print ("board-", end="") #happens if switch is open

    # read pin using bcm numbering system
    wiringpi2.wiringPiSetupSys()
    wiringpi2.pinMode(pin_boardpin_bcm,0)
    if wiringpi2.digitalRead(pin_boardpin_bcm):
        print ("BOARD-", end="") #happens if switch is closed
    else:
        print ("board-", end="") #happens if switch is open

    # read pin using wiringpi numbering system
    wiringpi2.wiringPiSetupGpio()
    wiringpi2.pinMode(pin_boardpin_wiringpi,0)
    if wiringpi2.digitalRead(pin_boardpin_wiringpi):
        print ("BOARD") #happens if switch is closed
    else:
        print ("board") #happens if switch is open
    

        
