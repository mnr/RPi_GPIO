import spidev
import time

spi=spidev.SpiDev()
spiDevice = spi.open(0,0)

while True:
    time.sleep(1)
    to_send = [0x01,0x02,0x03,0x04]
    resp = spi.xfer(to_send)
    print (resp)
    

