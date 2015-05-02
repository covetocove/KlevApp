import serial
import time

ser = serial.Serial('/dev/tty.usbmodem1421',9600,timeout=1)
ser.flushInput()
ser.flushOutput()
while 1:
    print("Testing this beech")
    print("Just did some sleeping")
    data_raw = ser.readline()
    print(data_raw)
