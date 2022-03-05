# Lora-E5-Circuitpython-P2P
P2P communication between two Grove Lora-E5 using Circuitpython

Usage Code.py:
1) Connect a pair of Grove LORA-E5 to two separate microcontroller
2) Copy code.py in each microcontroller
3) On the receiver open Serial and send this command
      AT+MODE=TEST
      AT+TEST=RXLRPKT
4) On transmiter microcontroller, open Serial and send This command. i.e send byte "AA"
      AT+MODE=TEST
      AT+TEST=TXLRPKT, "AA:
5) See console on receiver to confirm that the byte is received
6) Usage of Code-text sender.py & Code-text receiver.py description in the comment
7) Code-receiver-MQTT.py is example how to receive LORA P2P and then send the variable thru MQTT broker over TDP port 1883. using wifi esp8266 shield. 
