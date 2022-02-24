#This is sender code, tp rename to code.py and put into the sender micro-controller
#and then open serial and input the message, open new window & serial for another microcontroller for receiver
import board
import busio
import digitalio
import time
import supervisor
import binascii

uart = busio.UART(board.D6, board.D7, baudrate=9600) #to change the Pin according to micro-controller
get_input = True
message_started = False
message_print = []
allstring = ""
printshow = False
while True:
    if supervisor.runtime.serial_bytes_available:
        allstring=""
        b = "AT+TEST=TXLRPKT, \"3C"+bytes(binascii.hexlify(input().encode('utf-8'))).decode()+"3E\""
        b = bytes(b,'utf-8')
        #userinput.type()    
        #b = bytes(userinput, 'utf-8')
        #print(b)
        uart.write(bytes("AT+MODE=TEST",'utf-8'))
        time.sleep(2)
        uart.write(bytes("AT+TEST",'utf-8'))
        time.sleep(2)
        #print("Data Dalam bentuk 'byte' yang hendak dihantar")
        #print(b)
        uart.write(b)
        
        continue
    byte_read = uart.readline()# read up to 32 bytes
    if byte_read != None:
        allstring += byte_read.decode()
        printshow = True
    else:
        if printshow == True:
            if allstring != "":
                
                #print(allstring)
                left ='"3C'
                right ='3E"' 
                try:
                    dataRead =allstring[allstring.index(left)+len(left):allstring.index(right)]
                    print("\nData yang dihantar dalam bentuk 'bytes'")
                    print(b)
                    print("\nData dalam bentuk HEX:")
                    print(dataRead)
                    print("\nTukar data dari Hex kepada bentuk 'utf8' atau 'ASCII': ")
                    print(binascii.unhexlify(dataRead).decode('utf8'))
                    #print(b)            
                except ValueError:
                    print(ValueError)
                    pass
            allstring=""
            printshow ==False
