#rename to code.py Put This code into another Circuitpython microcontroller
#type MODE+TEST
#type AT+TEST
#monitor that the message is received in HEX and converted into String

import board
import busio
import digitalio
import time
import supervisor
import binascii
import re

uart = busio.UART(board.D0, board.D1, baudrate=9600)
get_input = True
message_started = False
message_print = []
allstring = ""
printshow = False
while True:
    if supervisor.runtime.serial_bytes_available:
        allstring=""
        userinput = input().strip()

        b = bytes(userinput, 'utf-8')
        uart.write(b)
        continue
    byte_read = uart.readline()# read up to 32 bytes
    if byte_read != None:
        allstring += byte_read.decode()
        printshow = True
    else:
        if printshow == True:
            if allstring != "":
                print(allstring)
                left ='"3C'
                right ='3E"' 
                try:
                    
                    b =allstring[allstring.index(left)+len(left):allstring.index(right)]
                    print(binascii.unhexlify(b).decode('utf8'))
                    #print(b)            
                except ValueError:
                    print(ValueError)
                    pass
                
                
            allstring=""
            printshow ==False
