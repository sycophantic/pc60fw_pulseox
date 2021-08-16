#!/usr/bin/python3

import matplotlib.pyplot as plt

x = []
y = []
xcount = 0

with open('raw_data.txt') as file:
    for line in file:
        line = line.rstrip()
        b = bytes.fromhex(line)
        s = b.find(b'\xaa\x55\x0f\x07\x02')
        if s >= 0:
            for loop in range(5):
                y.append(b[s+5+loop] & 127)
                x.append(xcount)
                ya = b[s+5+loop] & 127
                #plt.scatter(xcount, ya)
                xcount=xcount + 1
            #plt.pause(0.00001)
    print(y)
    print(x)
    plt.plot(x,y)
    plt.show()

