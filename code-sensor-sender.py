#rename to sensor sender module
#import semua library yang berkaitan
import time
import board
import busio
import adafruit_ssd1306
import adafruit_scd30
import digitalio
import time
import supervisor
import binascii


#mendefinisikan penggunaan i2C
i2c = board.I2C()
#mendefinisikan penggunaan UART
uart = busio.UART(board.D6, board.D7, baudrate=9600)
#mendefisikan objek oled
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
get_input = True
message_started = False
message_print = []
allstring = ""
printshow = False
#Mula Loop
# Sela Masa untuk membaca sensor
DELAY_DURATION = 5
# When we last changed the LED state
LAST_READSENSOR = 0

uart.write(bytes("AT+MODE=TEST",'utf-8'))
temperature = 30
while True:
    now = time.monotonic()
    if now >= LAST_READSENSOR + DELAY_DURATION: #periksa sekiranya lepas 5 saat
         #Baca bacaan sensor SCD30 
        scd = adafruit_scd30.SCD30(i2c)
        #print(scd.temperature)
        if scd.temperature != None: # Formatkan sekiranya ada bacaan sensor sahaja
            #Formatkan kepada dua titik perpuluhan
            temperature = "{:.2f}".format(scd.temperature)
            relative_humidity = "{:.2f}".format(scd.relative_humidity)
            co2_ppm_level = "{:.2f}".format(scd.CO2)
            sensorReading = temperature+","+relative_humidity+","+co2_ppm_level
        #print(temperature)
        allstring=""
        b = "AT+TEST=TXLRPKT, \"3C"+bytes(binascii.hexlify(sensorReading.encode('utf-8'))).decode()+"3E\""
        b = bytes(b,'utf-8') 
        oled.fill(0)
        #Lukis segiempat sama
        oled.rect(10, 10, oled.width-10, oled.height-10, True)     
        #paparkan pada OLED
        oled.text("https://sidik.my",20,20,1)
        oled.text("CO2      :" +co2_ppm_level, 20, 30,1)
        oled.text("Temp     :"+temperature, 20, 40, 1)
        oled.text("Humidity :"+relative_humidity, 20, 50, 1)
        oled.show()
        #print(b)
        uart.write(b)
        LAST_READSENSOR = now # RESET TIMER
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
                except ValueError as e:
                    print("ValueError:")
                    print(e)
                    pass
            allstring=""
            printshow ==False
