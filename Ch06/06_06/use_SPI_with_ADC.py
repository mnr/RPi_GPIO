# works with MCP3008, ch0
# returns x/10ths of a volt
import spidev
import time

spi=spidev.SpiDev() # create a spi object

spiBus = 0          # spi port 0
spiDeviceCh = 0       # GPIO CE0
spiDevice = spi.open(spiBus,spiDeviceCh)

# instructions for this value are found in the MCP3008 datasheet
# Table 5-2: Configure bits for the MCP3008
spiControl = 0b00001000 # single end mcp3008 ch0

to_send = [spiControl,0x02]

try:
    while True:
        time.sleep(1)
        resp = spi.xfer(to_send)
        print (resp)
except KeyboardInterrupt: #control-c
    spi.close()         # close the spi device
    

