import serial
import time
import threading

SERIAL_PATH = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75230313833351314221-if00"

def serial_do(is_read, message=None, ser=[]):
    if (len(ser) == 0):
        s = serial.Serial(SERIAL_PATH, 9600, timeout=1,
                            writeTimeout=1)
        ser.append(s)

        sem = threading.Semaphore(1)
        ser.append(sem)

    else:
        s = ser[0]
        sem = ser[1]

    ret = None
    sem.acquire()
    try:
        if (is_read):
            ret = serial_read(s)
        else:
            serial_write(s, message)
    except:
        print "exception :(\n"
    finally:
        sem.release()
    return ret

def serial_write(ser, message):
    ser.flushOutput()
    ser.flushInput()
    ser.write(message)

def serial_read(ser):
    data = ser.readline()
    return data



