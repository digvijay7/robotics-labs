#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

import signal
import sys

count = 0

def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

# handle the button event
def counter (pin):
    global count
    count += 1
    #print count
    if count >= 30:
        print "One revolution complete!"
        count = 0

# main function
def main():
    signal.signal(signal.SIGINT, signal_handler)
    # tell the GPIO module that we want to use 
    # the chip's pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # setup pin 23 as an input
    GPIO.setup(23,GPIO.IN)

    # tell the GPIO library to look out for an 
    # event on pin 23 and deal with it by calling 
    # the counter function
    GPIO.add_event_detect(23,GPIO.RISING,bouncetime=50)
    GPIO.add_event_callback(23,counter)

    while True:
        time.sleep(1)

    GPIO.cleanup()

if __name__=="__main__":
    main()
