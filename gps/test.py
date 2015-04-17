import serial
from pynmea import nmea

ser = serial.Serial('/dev/ttyAMA0',9600)
gpgga = nmea.GPGGA()
while 1:
     data = ser.readline()
     if (data.startswith('$GPGGA')):
         gpgga.parse(data)
         print 'Lat: ', gpgga.latitude
         print 'Long: ', gpgga.longitude
         print 'Alt: ', gpgga.antenna_altitude, ' ', gpgga.altitude_units
         print 'No of sats: ', gpgga.num_sats
