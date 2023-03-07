# code to demonstrate servos connected to PCA9685 via i2c
# Mark Niemann-Ross

from Servo import Servo
import smbus2
import bme280
from time import sleep

# BME280 initialization
# my thanks to joan on raspberrypi.org, topic 114401
for i2cbank in range(3): # test for i2c banks 0 and 1
    try:
        bus = smbus2.SMBus(i2cbank) # does bank 0 or 1 exist?
        break
    except:
        pass

if i2cbank == 2:
    print("i2c bank not found. Have you enabled i2c in raspbi-config?")
    exit()
    
# if this far, there is a valid i2c bank
# look for bme280 on 0x76 or 0x77
for address in range(128):
    try:
        bus.read_byte(address)
        if (address == 0x76 or address == 0x77):
            break
    except:
        pass
       
    
print("bme found at i2cbank: ", i2cbank,", i2c device id: ", hex(address))

# address = 0x76 # if "70: 70 -- -- -- -- -- 76 -- "
# address = 0x77 # if "70: 70 -- -- -- -- -- -- 77 "

calibration_params = bme280.load_calibration_params(bus, address)

# servo setup
temp_Servo = Servo(0) # position zero of the pca9685
temp_Servo.setup()
pres_Servo = Servo(15) # position 15 of the pca9685
pres_Servo.setup()

while True:
    temp_Servo.write(0) # send temp to 0
    pres_Servo.write(0) # send pressure to 0
    sleep(1)
    temp_Servo.write(180) # send temp to far end
    pres_Servo.write(180) # send pressure to end
    sleep(1)
    # take a single reading and return a compensated_reading
    data = bme280.sample(bus, address, calibration_params)
    
    # translate bme280 temperature into servo setting
    min_temp = -40 # servo: 1 = -40 (min temp)
    max_temp = 85 # servo: 179 = 85 (max temp)
    # 0 > x > 1 = (temp - min(temp) ) / ( max(temp) - min(temp) )
    # "1-" inverts the servo position so zero degrees is left, instead of right
    ServoPercent = 1-(data.temperature - min_temp) / (max_temp -  min_temp)
    ServoPosn = ServoPercent * 180 #
    print("temperature servo position: ",ServoPosn)
    temp_Servo.write(ServoPosn)

    # translate bme280 Barometric Pressure into servo setting
    min_press = 300 # servo: 1 = 300 (min pressu)
    max_press = 1100 # servo: 179 = 1100 (max humidity)
    # 0 > x > 1 = (temp - min(temp) ) / ( max(temp) - min(temp) )
    # "1-" inverts the servo position so zero degrees is left, instead of right
    ServoPercent = 1-(data.pressure - min_press) / (max_press -  min_press)
    ServoPosn = ServoPercent * 180 
    print("Pressure servo position: ",ServoPosn)
    pres_Servo.write(ServoPosn)
    
    # for reference on the console
    print(data)
    print()
    sleep(10) # pause between readings







