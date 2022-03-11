# Write your code here :-)
import board
import busio
import digitalio
import time
import supervisor
import json
import binascii
import math
import adafruit_scd30
#Set UART Pin
LCD_SDA = board.GP26 
LCD_SCL = board.GP27
i2c = busio.I2C(scl=LCD_SCL, sda=LCD_SDA)


# i2c = board.I2C() # untuk seeeduino, tidak perlu definisi I2C
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)
get_input = True
message_started = False
message_print = []
allstring = ""
printshow = False

def at_send_check_response(p_ack, timeout, p_cmd):
    b = bytes(p_cmd, 'utf-8')
    print(p_ack)
    print(b)
    uart.write(b)
    # delay(200)
    DELAY_DURATION = timeout
    LAST_TIME = 0
    now = time.monotonic()
    condition = True
    allstring=""
    while condition:
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
        condition = time.monotonic() - now < timeout
    return 0

at_send_check_response("AT",2,"AT")
at_send_check_response("AT",3,"AT+ID")
at_send_check_response("Set AT+MODE=LWOTAA",2,"AT+MODE=LWOTAA")
at_send_check_response("Set AT+DR=AS923",2,"AT+DR=AS923") # based on your gateway 
at_send_check_response("Set AT+APPKEY",2,"AT+KEY=APPKEY \"your app key here\"")
at_send_check_response("Set AT+CLASS=A",2,"AT+CLASS=A")
at_send_check_response("Set AT+PORT=8",2,"AT+PORT=8")
at_send_check_response("Set AT+JOIN",10,"AT+JOIN")

while True:    
    scd = adafruit_scd30.SCD30(i2c)
    if scd.temperature != None: # Formatkan sekiranya ada bacaan sensor sahaja
            #Formatkan kepada dua titik perpuluhan
            temperature = "{:.2f}".format(scd.temperature)
            relative_humidity = "{:.2f}".format(scd.relative_humidity)
            co2_ppm_level = "{:.2f}".format(scd.CO2)
            brokers_out={'C':co2_ppm_level,'T':temperature,'H':relative_humidity}
    print(brokers_out)
    data_out=json.dumps(brokers_out)
    send_string= "AT+CMSGHEX="+bytes(binascii.hexlify(data_out.encode('utf-8'))).decode()+""    
    at_send_check_response("Sending", 30, send_string)
    
    time.sleep(60)
