import json
import serial
from time import sleep

def arduino_serial_comm(port, character):
    # Define the data file (json):
    json_file = 'assets/villagers.json'
    # Define the build-in Arduino Leonardo port on the LattePanda:
    arduino = serial.Serial(port, 9600, timeout=1)
    # Elicit information:
    with open (json_file) as data:
        villagers = json.load(data)
        c = villagers[character]
        msg = "Character: {}\n\nBirthday: {}\n\nLoves: {}\n\nLikes: {}\n\nHates: {}".format(character, c['birthday'], c['loves'], c['likes'], c['hates'])
        print(msg)
        arduino.write(msg.encode())
        sleep(1)
        