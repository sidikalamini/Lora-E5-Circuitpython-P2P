# Lora-E5-Circuitpython-P2P
P2P communication between two Grove Lora-E5 modules using CircuitPython

Usage Code.py:
1) Connect a pair of Grove LORA-E5 to two separate microcontrollers
2) Copy code.py in each microcontroller
3) On the receiver open Serial and send this command
      AT+MODE=TEST
      AT+TEST=RXLRPKT
4) On transmiter microcontroller, open Serial and send This command. i.e send byte "AA"
      AT+MODE=TEST
      AT+TEST=TXLRPKT, "AA:
5) See console on receiver to confirm that the byte is received
6) Usage of code-text-sender.py & code-text-receiver.py in the comment, used to send full text string. we are using binascii hexlify and unhexlify 
7) code-sensor-receiver.py and code-sensor-sender.py is an example how to send sensor data thru P2P LORA-E5
8) code-receiver-MQTT.py is an example how to receive LORA P2P and then send the variable thru MQTT broker over TDP port 1883. Using wifi esp8266 shield. 
