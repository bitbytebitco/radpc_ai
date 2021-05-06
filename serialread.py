#!/usr/bin/env python3
import serial

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

if __name__ == '__main__':
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    ser.flush()

    while True:
        try:
            if ser.in_waiting > 0:
                print(ser.read())
                command = ser.read() # read a single byte
                if(command == b'\x24'):
                    command = b'\x24' # '$' character in hex
                    ser.write(command) # respond with received byte
                    ser.flush()
                else:
                    packet = ser.readline().decode('ascii') # receive packet 
                    print(packet)
        except Exception as e:
            print('error')
            print(e)
