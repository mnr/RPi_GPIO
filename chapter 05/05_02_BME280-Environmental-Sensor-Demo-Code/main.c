/*
  Comple：make
  Run: ./bme280
  
  This Demo is tested on Raspberry PI 3B+
  you can use I2C or SPI interface to test this Demo
  When you use I2C interface,the default Address in this demo is 0X77
  When you use SPI interface,PIN 27 define SPI_CS
*/
/*
 * MNR Notes
 * I've configured this for SPI
 * Connections for the waveshare BME280 are...
 * Power - VCC - red wire - RPi board 1 - 3.3vdc
 * Ground - gnd - black wire - RPi board 6 - ground
 * SPI Data In - MOSI - Blue - RPi board 19 - SPI0 MOSI GPIO10
 * SPI Clock - SCK - yellow - RPi board 23 - SPI0 SCLK GPIO 11
 * SPI Data Out - MISO - orange - RPi board 21 - SPI0 MISO GPIO09
 * SPI Chip Select - CS - green - RPi Board 36 - GPIO16 wiring pi 27
 * Note: Waveshare refers to pins using the wiringpi scheme. 
*/

#include "bme280.h"
#include <stdio.h>
#include <unistd.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>

//Raspberry 3B+ platform's default SPI channel
#define channel 0  

//Default write it to the register in one time
#define USESPISINGLEREADWRITE 1

//This definition you use I2C or SPI to drive the bme280
//When it is 1 means use I2C interface, When it is 0,use SPI interface
#define USEIIC 0


#if(USEIIC)
#include <string.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <fcntl.h>
//Raspberry 3B+ platform's default I2C device file
#define IIC_Dev  "/dev/i2c-1"
	
int fd;

void user_delay_ms(uint32_t period)
{
  usleep(period*1000);
}

int8_t user_i2c_read(uint8_t id, uint8_t reg_addr, uint8_t *data, uint16_t len)
{
  write(fd, &reg_addr,1);
  read(fd, data, len);
  return 0;
}

int8_t user_i2c_write(uint8_t id, uint8_t reg_addr, uint8_t *data, uint16_t len)
{
  int8_t *buf;
  buf = malloc(len +1);
  buf[0] = reg_addr;
  memcpy(buf +1, data, len);
  write(fd, buf, len +1);
  free(buf);
  return 0;
}
#else

// When you use SPI interface,PIN 27 define SPI_CS
#define SPI_CS 27

void SPI_BME280_CS_High(void)
{
	digitalWrite(SPI_CS,1);
}

void SPI_BME280_CS_Low(void)
{
	digitalWrite(SPI_CS,0);
}

void user_delay_ms(uint32_t period)
{
  usleep(period*1000);
}

int8_t user_spi_read(uint8_t dev_id, uint8_t reg_addr, uint8_t *reg_data, uint16_t len)
{
	int8_t rslt = 0;
	
	SPI_BME280_CS_High();
	SPI_BME280_CS_Low();
	
	wiringPiSPIDataRW(channel,&reg_addr,1);

	#if(USESPISINGLEREADWRITE)
    for(int i=0; i < len ; i++)
	{
	  wiringPiSPIDataRW(channel,reg_data,1);
	  reg_data++;
	}
	#else
	wiringPiSPIDataRW(channel,reg_data,len);
	#endif
	
	SPI_BME280_CS_High();
	
	return rslt;
}

int8_t user_spi_write(uint8_t dev_id, uint8_t reg_addr, uint8_t *reg_data, uint16_t len)
{
	int8_t rslt = 0;

	SPI_BME280_CS_High();
	SPI_BME280_CS_Low();

	wiringPiSPIDataRW(channel,&reg_addr,1);
	
	#if(USESPISINGLEREADWRITE)
	for(int i = 0; i < len ; i++)
	{
		wiringPiSPIDataRW(channel,reg_data,1);
		reg_data++;
	}
	#else
	wiringPiSPIDataRW(channel,reg_data,len);
	#endif
	
	SPI_BME280_CS_High();
	
	return rslt;
}
#endif

void print_sensor_data(struct bme280_data *comp_data)
{
#ifdef BME280_FLOAT_ENABLE
	printf("temperature:%0.2f*C   pressure:%0.2fhPa   humidity:%0.2f%%\r\n",comp_data->temperature, comp_data->pressure/100, comp_data->humidity);
#else
	printf("temperature:%ld*C   pressure:%ldhPa   humidity:%ld%%\r\n",comp_data->temperature, comp_data->pressure/100, comp_data->humidity);
#endif
}

int8_t stream_sensor_data_forced_mode(struct bme280_dev *dev)
{
    int8_t rslt;
    uint8_t settings_sel;
    struct bme280_data comp_data;

    /* Recommended mode of operation: Indoor navigation */
    dev->settings.osr_h = BME280_OVERSAMPLING_1X;
    dev->settings.osr_p = BME280_OVERSAMPLING_16X;
    dev->settings.osr_t = BME280_OVERSAMPLING_2X;
    dev->settings.filter = BME280_FILTER_COEFF_16;

    settings_sel = BME280_OSR_PRESS_SEL | BME280_OSR_TEMP_SEL | BME280_OSR_HUM_SEL | BME280_FILTER_SEL;

    rslt = bme280_set_sensor_settings(settings_sel, dev);

    printf("Temperature           Pressure             Humidity\r\n");
    /* Continuously stream sensor data */
    while (1) {
        rslt = bme280_set_sensor_mode(BME280_FORCED_MODE, dev);
        /* Wait for the measurement to complete and print data @25Hz */
        dev->delay_ms(40);
        rslt = bme280_get_sensor_data(BME280_ALL, &comp_data, dev);
        print_sensor_data(&comp_data);
    }
    return rslt;
}


int8_t stream_sensor_data_normal_mode(struct bme280_dev *dev)
{
	int8_t rslt;
	uint8_t settings_sel;
	struct bme280_data comp_data;

	/* Recommended mode of operation: Indoor navigation */
	dev->settings.osr_h = BME280_OVERSAMPLING_1X;
	dev->settings.osr_p = BME280_OVERSAMPLING_16X;
	dev->settings.osr_t = BME280_OVERSAMPLING_2X;
	dev->settings.filter = BME280_FILTER_COEFF_16;
	dev->settings.standby_time = BME280_STANDBY_TIME_62_5_MS;

	settings_sel = BME280_OSR_PRESS_SEL;
	settings_sel |= BME280_OSR_TEMP_SEL;
	settings_sel |= BME280_OSR_HUM_SEL;
	settings_sel |= BME280_STANDBY_SEL;
	settings_sel |= BME280_FILTER_SEL;
	rslt = bme280_set_sensor_settings(settings_sel, dev);
	rslt = bme280_set_sensor_mode(BME280_NORMAL_MODE, dev);

	printf("Temperature           Pressure             Humidity\r\n");
	while (1) {
		/* Delay while the sensor completes a measurement */
		dev->delay_ms(70);
		rslt = bme280_get_sensor_data(BME280_ALL, &comp_data, dev);
		print_sensor_data(&comp_data);
	}

	return rslt;
}

#if(USEIIC)
int main(int argc, char* argv[])
{
  struct bme280_dev dev;
  int8_t rslt = BME280_OK;

  if ((fd = open(IIC_Dev, O_RDWR)) < 0) {
    printf("Failed to open the i2c bus %s", argv[1]);
    exit(1);
  }
  if (ioctl(fd, I2C_SLAVE, 0x77) < 0) {
    printf("Failed to acquire bus access and/or talk to slave.\n");
    exit(1);
  }
  //dev.dev_id = BME280_I2C_ADDR_PRIM;//0x76
  dev.dev_id = BME280_I2C_ADDR_SEC; //0x77
  dev.intf = BME280_I2C_INTF;
  dev.read = user_i2c_read;
  dev.write = user_i2c_write;
  dev.delay_ms = user_delay_ms;

  rslt = bme280_init(&dev);
  printf("\r\n BME280 Init Result is:%d \r\n",rslt);
  //stream_sensor_data_forced_mode(&dev);
  stream_sensor_data_normal_mode(&dev);
}
#else
int main(int argc, char* argv[])
{
  if(wiringPiSetup() < 0)
  {
    return 1;
  }
  
  pinMode (SPI_CS,OUTPUT) ;
  
  SPI_BME280_CS_Low();//once pull down means use SPI Interface
  
  wiringPiSPISetup(channel,2000000);

  struct bme280_dev dev;
  int8_t rslt = BME280_OK;

  dev.dev_id = 0;
  dev.intf = BME280_SPI_INTF;
  dev.read = user_spi_read;
  dev.write = user_spi_write;
  dev.delay_ms = user_delay_ms;

  rslt = bme280_init(&dev);
  printf("\r\n BME280 Init Result is:%d \r\n",rslt);
  //stream_sensor_data_forced_mode(&dev);
  stream_sensor_data_normal_mode(&dev);
}
#endif
