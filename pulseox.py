#!/usr/bin/python3

import struct
from bluepy.btle import *
from datetime import datetime
import csv
import time

tsname = datetime.now().strftime("%Y%m%d-%H%M%S")
stack= []

# callback class
class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
      ts = str(datetime.now())
      if len(data) == 20:
        with open('spo2_' + tsname + '.csv', 'a', newline='') as out:
          w = csv.writer(out, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
          ds = data.find(b'\x0f\x08\x01')
          if ds >= 0 and ds <= 14:
            spo2 = data[ds + 3]
            pulse = data[ds + 4] + (data[ds + 5] << 8)
            pi = data[ds + 6] / 10
            output=[ts, spo2, pulse, pi, bytes(data).hex()]
            print(output)
            w.writerow(output)
          if stack:
            pulse=stack.pop() + (data[0] << 8)
            spo2=stack.pop()
            pi = data[1] / 10
            output=[ts, spo2, pulse, pi, bytes(data).hex()]
            print(output)
            w.writerow(output)
          if ds == 15:
            stack.append(data[ds + 3])
            stack.append(data[ds + 4])
        #with open('spo2_' + tsname + '.csv', 'a', newline='') as out:
        #w = csv.writer(out, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #rb = bytes(data).hex()
        #ts = str(datetime.now())

          

def receive():

# connect to device
  #per = Peripheral("MAC HERE", "random")

  try:
      print('Connecting')
      per = Peripheral("MAC HERE", "random")

      # set callback for notifications
      per.setDelegate(MyDelegate())

    # enable notification
      setup_data = b"\x01\x00"
      notify = per.getCharacteristics(uuid='6e400003-b5a3-f393-e0a9-e50e24dcca9e')[0]
      notify_handle = notify.getHandle() + 1
      per.writeCharacteristic(notify_handle, setup_data, withResponse=True)
    
    # send test string
    #c = per.getCharacteristics(uuid='6e400002-b5a3-f393-e0a9-e50e24dcca9e')[0]
    #c.write("Hello Gecko")
    
    # wait for answer
      while True:
          if per.waitForNotifications(0.1):
              continue
  except BTLEDisconnectError:
     print('Disconnected')
     time.sleep(0.1)
     receive()
  except:
     print('some other exception')
     time.sleep(0.1)
     receive()
  finally:
      per.disconnect()

receive()
