# what do decimal numbers look like when converted to binary
for aNumber in range(16):
    # testing a number for zero or not
    if (aNumber & 0b1000 > 0):
        led8value = "led ON"
    else:
        led8value = "led OFF"
        
    print("decimal:\t", aNumber,
          "\tbinary:\t",format(aNumber, 'b').zfill(4),
          "\tLED 8:\t", led8value,
          "\tLED 4:\t", aNumber & 4,
          "\tLED 2:\t", aNumber & 2,
          "\tLED 1:\t", aNumber & 1,
          )
