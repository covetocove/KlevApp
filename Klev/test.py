import serial
import time

SERIAL_PATH = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75230313833351314221-if00"

ser = serial.Serial(SERIAL_PATH,9600,timeout=1)
ser.flushInput()
ser.flushOutput()
while 1:
    data_raw = ser.readline()
    print(data_raw)
