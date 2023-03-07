# what do decimal numbers look like when converted to binary
for aNumber in range(16):
    print("decimal:\t", aNumber,
          "\tbinary:\t",format(aNumber, 'b').zfill(4),
          "\tLED 8:\t", "unknown",
          )

# change "unknown" to aNumber & 0b1000