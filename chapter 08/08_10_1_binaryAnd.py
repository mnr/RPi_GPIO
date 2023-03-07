# what do decimal numbers look like when converted to binary
for aNumber in range(16):
    print("decimal:\t", aNumber, "\tbinary:\t",format(aNumber, 'b').zfill(4))