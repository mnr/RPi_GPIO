/* 09-07_c_gpio.c
 * 
 * Demonstration of controlling the Raspberry Pi GPIO with C
 * 
 * 1) install bcm2835 (http://www.airspayce.com/mikem/bcm2835/index.html)
 * 2) cd directory-containing-this-file
 * 3) compile ... gcc -o bincount 09-07_c_gpio.c -l bcm2835
 * 4) ./bincount
 * 
 * Author: Mark Niemann-Ross
 * https://linkedin.com/in/markniemannross
 */


#include <bcm2835.h>
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>

/* set up bank of LEDs
 * BCM 26 is MSB. BCM 21 is LSB
*/
#define LED_1 RPI_V2_GPIO_P1_40 // aka BCM 21
#define LED_2 RPI_V2_GPIO_P1_38 // aka BCM 20
#define LED_4 RPI_V2_GPIO_P1_36 // aka BCM 16
#define LED_8 RPI_V2_GPIO_P1_37 // aka BCM 26
#define resetbutton RPI_V2_GPIO_P1_05 // aka BCM 3

void LightsOn( int lightMask ) {
    // bcm2835_gpio_write(PIN, HIGH); turns on a pin
    // HIGH = 1
    bcm2835_gpio_write(LED_1, lightMask & 1 );
    bcm2835_gpio_write(LED_2, lightMask & 2 );
    bcm2835_gpio_write(LED_4, lightMask & 4 );
    bcm2835_gpio_write(LED_8, lightMask & 8 );
}

void ctlcHandler( int sig) {
    LightsOn(0);
    bcm2835_close();
    exit(0);
}

int main(int argc, char **argv)
{

    if (!bcm2835_init())
      return 1;
      
    signal(SIGINT, ctlcHandler);

    // Set the LED pins to output
    bcm2835_gpio_fsel(LED_1, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(LED_2, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(LED_4, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(LED_8, BCM2835_GPIO_FSEL_OUTP);
    
    // set the resetbutton to input
    bcm2835_gpio_fsel(resetbutton, BCM2835_GPIO_FSEL_INPT);
    //  with a pullup
    bcm2835_gpio_set_pud(resetbutton, BCM2835_GPIO_PUD_UP);

    
    int counter;

    while (1)
    {
	counter = 0;
	while (counter < 16 ) {
	    while ( !bcm2835_gpio_lev(resetbutton) ) {
		printf("reset button pushed\n");
		LightsOn(15);
		counter = 0;
	    }
			
	    LightsOn( counter );
			
	    counter++;
			
	    delay(1000);
	}
    }
}

