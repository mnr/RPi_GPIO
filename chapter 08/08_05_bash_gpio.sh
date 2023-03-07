#!/bin/bash

# the GPIO requires root level access. So...
# cd to exercise files
# then...
# sudo bash ./09-05_bash_gpio.sh

# bash shell script to demonstrate gpio control

# set up pushbutton
resetbutton=3 # BCM numbering scheme 
echo $resetbutton > /sys/class/gpio/export
echo "in" > "/sys/class/gpio/gpio${resetbutton}/direction"
echo "assign GPIO pin $resetbutton as pushbutton"

# set up bank of LEDs
# pin 26 is MSB. pin 21 is LSB
# so ${LED_pins[0]} points to gpio pin 21, which is least significant bit (LSB)
LED_pins=(21 20 16 26) # BCM numbering scheme. 
LED_paths=() # creating an array for use in a minute

# Assign GPIO pins to LEDs
for LED_idx in {0..3}
do
	echo "assign GPIO pin ${LED_pins[$LED_idx]} as LED"
	echo ${LED_pins[$LED_idx]} > /sys/class/gpio/export
	LED_paths[$LED_idx]="/sys/class/gpio/gpio${LED_pins[$LED_idx]}/"
	echo "out" > "${LED_paths[$LED_idx]}direction"
done

# create and install function to clean up pin assignments on control+c
echo "press CTRL+C to stop..."
function controlC {
	echo
	for LED_idx in {0..3}
	do
		echo "Clean up GPIO pin ${LED_pins[$LED_idx]}"
		echo ${LED_pins[$LED_idx]} > /sys/class/gpio/unexport
	done
	echo "Clean up GPIO pin $resetbutton"
	echo $resetbutton > /sys/class/gpio/unexport
	exit $?
}
trap controlC SIGINT

# function to turn on/off LEDs
function LightsOn ( ) {
	# $1 is the argument passed to LightsOn. i.e LightsOn($1)
	echo $(($1 & 2#0001)) > "${LED_paths[0]}value"
	echo $(($1 & 2#0010)) > "${LED_paths[1]}value"
	echo $(($1 & 2#0100)) > "${LED_paths[2]}value"
	echo $(($1 & 2#1000)) > "${LED_paths[3]}value"
}

# this is the working loop
while :
do
	counter=0
	while [ $counter -lt 16 ]
	do
		# test for pushbutton
		if [[ $(< "/sys/class/gpio/gpio${resetbutton}/value") == "0" ]]
		then
			LightsOn 15 # turn on all the LEDs
			while [[ $(< "/sys/class/gpio/gpio${resetbutton}/value") == "0" ]] 
			do
				echo "waiting while button is pressed"
			done
			counter=0 # restart the count from zero
			echo "The button is released"
		fi
		LightsOn $counter
		sleep 1
		((counter++))
	done
done



