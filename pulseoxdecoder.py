#!/usr/bin/python3

from crccheck.crc import Crc8MaximDow

class decode(object):
  def __init__(self, raw):
    data = bytes.fromhex(raw)
    self.type = -1
    #if len(data) > 12:
    #  self.case = data[4]
    #  self.bytevalue = data[2]
    #  if self.case <= 12:
    #    if self.bytevalue == 15 and self.case == 1 and Crc8MaximDow.calc(data[0:11]) == data[11]: #reading
    #      self.type = 1
    #      self.spo2 = data[5]
    #      self.pulse = data[6] + (data[7] << 8)
    #      self.pi = data[8] / 10
    #    if self.case == 2 and data[14] == 8:
    #      self.type = 1
    #      self.spo2 = data[16]
    #      self.pulse = data[17] + (data[18] << 8)
    #      self.pi = data[19] / 10  
        
        #if self.case == 2 and self.bytevalue == 15:
        #  self.type = 2
        #  self.wave = data[5], data[6], data[7], data[8], data[9]

    
    if len(data) == 20:
      ds = data.find(b'\x0f\x08\x01') 
      if ds >= 0 and ds <= 14:
        self.type = 1
        self.spo2 = data[ds + 3]
        self.pulse = data[ds + 4] + (data[ds + 5] << 8)
        self.pi = data[ds + 6] / 10
      if ds == 14:
        self.type = 1
        self.spo2 = data[ds + 5]
        self.pulse = ''
        self.pi = ''

      self.case = -1
      self.bytevalue = -1
    else:
      self.case = -1
      self.bytevalue = -1
