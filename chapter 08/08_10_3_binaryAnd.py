# what do decimal numbers look like when converted to binary
for aNumber in range(16):
    print("decimal:\t", aNumber,
          "\tbinary:\t",format(aNumber, 'b').zfill(4),
          "\tLED 8:\t", aNumber & 0b1000,
          "\tLED 4:\t", aNumber & 0b0100,
          "\tLED 2:\t", aNumber & 0b0010,
          "\tLED 1:\t", aNumber & 0b0001,
          )
