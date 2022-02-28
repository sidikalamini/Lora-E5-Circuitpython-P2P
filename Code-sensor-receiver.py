#Rename to code.py and put in receiver module
# Write your code here :-)
# import semua library yang berkaitan
import time
import board
import busio
import binascii
import sys
import re
import adafruit_ssd1306

# mendefinisikan penggunaan UART
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

LCD_SDA = board.GP16
LCD_SCL = board.GP17
i2c = busio.I2C(scl=LCD_SCL, sda=LCD_SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

message_started = False
message_print = []
allstring = ""
printshow = False

# Mula Loop
# Setup AT+TEST=RXLRPKT
uart.write(bytes("AT+MODE=TEST", "utf-8"))
print("Checking.. AT+MODE=TEST")
while uart.readline():
    print(uart.readline())
uart.write(bytes("AT+TEST=?", "utf-8"))
print("Checking.. AT+TEST=TEST=?")
while uart.readline():
    print(uart.readline())

uart.write(bytes("AT+TEST=RXLRPKT", "utf-8"))
print("Checking.. AT+TEST=RXLRPKT")
while uart.readline():
    print(uart.readline())


while True:
    try:
        byte_read = uart.readline()  # read up to 32 bytes
        if byte_read:
            allstring += byte_read.decode()
            printshow = True
        else:
            if printshow:
                if allstring:
                    left = '"3C'
                    right = '3E"'
                    dataRead = re.search(
                        r"" + left + "(.*?)" + right + "", allstring
                    ).group(1)
                    clearstring = binascii.unhexlify(dataRead).decode("utf8")
                    print(clearstring)
                    letter_list = clearstring.split(",")
                    temperature = letter_list[0]
                    humidity = letter_list[1]
                    co2 = letter_list[2]
                    oled.fill(0)
                    #Lukis segiempat sama
                    oled.rect(10, 10, oled.width-10, oled.height-10, True)     
                    #paparkan pada OLED
                    oled.text("Demo RX Receiving",20,20,1)
                    oled.text("CO2      :" +co2, 20, 30,1)
                    oled.text("Temp     :"+temperature, 20, 40, 1)
                    oled.text("Humidity :"+humidity, 20, 50, 1)
                    oled.show()
                allstring = ""
                printshow = False
    except ValueError as e:
        # print(e)
        continue
    except AttributeError as ea:
        # print(ea)
        continue
    except KeyboardInterrupt:
        sys.exit()
