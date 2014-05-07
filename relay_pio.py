#!/usr/bin/python

import smbus
import time 

bus = smbus.SMBus(1)  #for revision 2 board...use 1

#Set the address (can check using i2cdetect -y 1 )
address = 0x20

# Set all banks to outputs
bank0 = 0 #Contains just power for relay board
bank1 = 1 #Contains all relays
bus.write_byte_data(address,0x00,0x00) # BankA outputs 
bus.write_byte_data(address,0x01,0x00) # BankB outputs

relay0 = 0
relay1 = 1
relay2 = 2
relay3 = 4
relay4 = 8
relay5 = 16
relay6 = 32 
relay7 = 64
relay8 = 128
relay = [0,1,2,4,8,16,32,64,128]

def set_relay(data,bank):

  print "set_relay bank=" + str(bank) + " data=" + str(data) 
  if bank == 1:
#     data = int(255 - data) # We only want to switch on one relay at a time
     bus.write_byte_data(address,0x12,data)
  elif bank == 0:
     bus.write_byte_data(address,0x13,data)
  else:
     print ("Something has gone horribly wrong")
     exit()
  time.sleep(1)
  return
  
def main():
   set_relay(relay[0],bank0) #switch off relay board
   set_relay(relay[0],bank1) #switch off relays
   print "Switching on relay1, bank0"
   set_relay(1,bank0) #switch on relay board
   counter = 0;
   while counter<8:
       this_relay=int(relay[counter])
       set_relay(this_relay,bank1)
       set_relay(relay0,bank1) #clear relays
       counter += 1
   print ("Cleaning up")
   set_relay(254,bank0) #switch off relay board
   set_relay(relay[0],bank0) #switch off relay board
   set_relay(relay[0],bank1) #switch off relay board
 
if __name__ == "__main__":
   main()
