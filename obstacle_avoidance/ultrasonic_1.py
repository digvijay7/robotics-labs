#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# ultrasonic_1.py
# Measure distance using an ultrasonic module
#
# Author : Matt Hawkins
# Date   : 09/01/2013
# -----------------------

import RPi.GPIO as GPIO
import time

import signal
import sys

THRESHOLD_DIST = 40 # in cm
FORWARD_TIME = 0.5
TURN_TIME = 0.5
SETTLE_TIME = 0.002
TRIGGER_TIME = 0.001

H1 = 9
H2 = 11
H3 = 8
H4 = 7
PINS = [H1,H2,H3,H4]

def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

class UltraSonicSensor():
    def __init__(self, trigger, echo, name):
    	print " Constructor"
        self.trigger = trigger
        self.echo = echo
        self.distance = -1
        self.name = name
        GPIO.setup(self.trigger,GPIO.OUT)  # Trigger
        GPIO.setup(self.echo,GPIO.IN)      # Echo
        GPIO.output(self.trigger, False)
        # Allow module to settle
        time.sleep(SETTLE_TIME)
        
#    def __del__(self):
#       GPIO.cleanup()

    def fire(self):
        print "fire " + self.name
        GPIO.output(self.trigger, True)
        time.sleep(TRIGGER_TIME)
        GPIO.output(self.trigger, False)
        start = time.time()
        stop = start
        #start2 = start
        flag = 0
        #print self.echo
        while GPIO.input(self.echo)==0:
            #print "waiting for echo"
            start = time.time()
#            if start - stop > 1000:
#                flag += 1
#                break
        #stop2 = start
        while GPIO.input(self.echo)==1:
            stop = time.time()
#            if stop - start > 1000:
#                flag += 2
#                break
        print flag
        elapsed = stop-start

        distance = elapsed * 34300

        self.distance = distance / 2
        return self.distance

    
def off(pin):
    GPIO.output(pin, False)


def on(pin):
    GPIO.output(pin, True)


def off_all():
    for x in PINS:
        off(x)
    #[off(x) for x in PINS]

def move_generic(pin1, pin2, move_time):
    off_all()
    time.sleep(0.001)
    on(pin1)
    on(pin2)
    time.sleep(move_time)
    off_all()
   
def move_forward(move_time):
    move_generic(H1,H3,move_time)

def move_backward(move_time):
    move_generic(H2,H4,move_time)

def turn_left(turn_time):
    move_generic(H2,H3,turn_time)

def turn_right(turn_time):
    move_generic(H1,H4,turn_time)

def init_hbridge():
    for pin in PINS:
	GPIO.setup(pin,GPIO.OUT)



def main():
    print "H"
    signal.signal(signal.SIGINT, signal_handler)
    
    #Use BCM GPIO references
    #instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)

    # TODO: Handle Ctrl-C

    init_hbridge()

    frontRight = UltraSonicSensor(23, 17, "right")
    frontLeft = UltraSonicSensor(22, 14,"left")
#    frontCentre = UltraSonicSensor(23, 24)

    us_sensors = [frontLeft,frontRight]

#    turn_right(FORWARD_TIME)
#    GPIO.cleanup()

    while(True):
        print "loop" 
        min_dist = 1000
        for sensor in us_sensors:
            dist = sensor.fire()
#            time.sleep(1)
            print "Distance: ", dist
            if dist < min_dist:
                min_dist = dist


        if min_dist < THRESHOLD_DIST:
            # Turn - Direction?
            turn_left(TURN_TIME)
#
        else:
            move_forward(FORWARD_TIME) # Should be function of min_dist


if __name__ == "__main__":
    main()
