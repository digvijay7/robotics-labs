#include <linux/i2c-dev.h>
#include <linux/i2c.h>
#include <fcntl.h>
#include <stdio.h>

int deviceHandle;
char buffer[11];

int main (void)
{
  // initialize buffer
  buffer[0] = 1;

  // open device on /dev/i2c-0
  deviceHandle = open("/dev/i2c-1", O_RDWR);

  // connect to arduino as i2c slave
  int deviceI2CAddress = 0x04;  
  ioctl(deviceHandle, I2C_SLAVE, deviceI2CAddress);

  // begin transmission and request acknowledgement
  write(deviceHandle, buffer, 1);
  sleep(1);
  read(deviceHandle,  buffer, 8);
  //buffer[10] = '\0';
  //buffer[9]='a';
  buffer[5]='\0';
  int i;
  sscanf(buffer, "%d", &i);
  printf("Received:%d\n",i);
  // close connection and return
  close(deviceHandle);
  return 0;
}
