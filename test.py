#!/usr/bin/python3
import csv
import pulseoxdecoder as po

ts='test'

with open('raw_data.txt') as file:
  with open('spo2' + ts + '.csv', 'w', newline='') as out:
    w = csv.writer(out, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for line in file:
        row = line.rstrip()
        r = po.decode(row)
        if r.type == 1:
          print ('Pulse:', r.pulse, 'SpO2:', r.spo2, 'Pi:', r.pi, 'Raw:', row, r.case)
          w.writerow([row, r.pulse, r.spo2, r.pi])
        else:
          print('Unknown data', 'Raw:', row, r.case)
          w.writerow([row, 'unk', r.case])

#data = 'aa550f08016239004400c0e3aa55f0030303f6aa'
#r = po.decode(data)
#if r.type == 1:
#    print ('Pulse:', r.pulse, 'SpO2:', r.spo2, 'Pi:', r.pi)
