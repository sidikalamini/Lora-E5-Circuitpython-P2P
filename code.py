import board
import busio
import digitalio
import time
import supervisor
#Set UART Pin
uart = busio.UART(board.D0, board.D1, baudrate=9600)
get_input = True
message_started = False
message_print = []
allstring = ""
printshow = False
while True:
    if supervisor.runtime.serial_bytes_available:
        allstring=""
        userinput = input().strip() #input command
        b = bytes(userinput, 'utf-8')
        uart.write(b)
        continue
    byte_read = uart.readline()# read one line
    if byte_read != None:
        allstring += byte_read.decode()
        printshow = True
    else:
        if printshow == True:
            if allstring != "":
                print(allstring)
            allstring=""
            printshow ==False

