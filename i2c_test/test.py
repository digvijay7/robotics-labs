import smbus
import time
import signal
import sys

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)
var = 1
time.sleep(1)
# This is the address we setup in the Arduino Program
address = 0x04
off = 0
flag = False
def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    global off
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    #number = bus.read_block_data(address,0)
    print number
    return number

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    if flag :
        readNumber()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    writeNumber(var)
    flag = True
    time.sleep(0.1)
    readNumber()
    flag = False
    var += 1
    if var == 6:
        var = 1
