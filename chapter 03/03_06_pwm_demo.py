# demonstrate the effects of frequency and duty cycle on Pulse Width Modulation

# Build this circuit on the Raspberry Pi
# 1) Turn off power to the Raspberry Pi
# 2) Connect GPIO12 (pin 32) to speaker
# 3) Connect speaker gnd to Raspberry Pi gnd (pin 34)
# 4) Connect GPIO13 (pin 33) to LED
# 5) Connect LED gnd to Raspberry Pi gnd (pin 39)
# 6) Connect Power to Raspberry Pi
# 7) cd to exercise files folder where ch04-06_pwm_demo.gif is found
# 8) windows - py ch04_pwm_demo.py

# imports
import RPi.GPIO as GPIO
import tkinter as tk

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# output pwm via GPIO12 (pin 32) and GPIO13 (pin 33)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
pwmToSpeaker = GPIO.PWM(12, 50) # GPIO12, frequency = 50Hz
pwmToSpeaker.start(0) # start PWM with duty cycle = 0
pwmToLED = GPIO.PWM(13, 50) # GPIO13, frequency = 50Hz
pwmToLED.start(0) # start PWM with duty cycle = 0

locationOfBackground = "03_06_pwm_demo.gif"

# set up tkinter
master = tk.Tk()
master.title("PWM demonstration")
windowWidth = 1000
windowHeight = 564
geomString = str(windowWidth) + "x" + str(windowHeight)
master.geometry(geomString)
# place background image
bgImagePh = tk.PhotoImage(file = locationOfBackground)
photoL = tk.Label(image=bgImagePh)
photoL.image = bgImagePh # thwart python garbage collection
photoL.place(x = 0, y = 0, relwidth=1, relheight=1)
# display values for frequency and duty cycle
pwm_freq_label = tk.Label(master, text="PWM Frequency=0")
pwm_freq_label.place(x = 560, y = 10)
pwm_dc_label = tk.Label(master, text="PWM Duty Cycle=0")
pwm_dc_label.place(x = 560, y = 30)

def motion(event):
    global master
    global pwmToSpeaker, pwmToLED
    pwm_frequency, pwm_dutyCycle = event.x, event.y # frequency = x, duty cycle = y
   
    # change frequency
    boxLeft = 557
    boxRight = 944
    maxFreq = 10000
    if boxLeft < pwm_frequency < boxRight:
        # convert mouse position x to frequency from 0 <- freq <- maxFreq
        pwm_frequency = int(maxFreq * ((pwm_frequency - boxLeft) / (boxRight - boxLeft)))
        pwmToSpeaker.ChangeFrequency(pwm_frequency)
        pwmToLED.ChangeFrequency(pwm_frequency)
        pwm_freq_label.config(text="PWM Frequency=" + str(pwm_frequency))
        pwm_freq_label.update_idletasks()

    # change duty cycle
    boxTop = 126
    boxBottom = 495
    if boxTop < pwm_dutyCycle < boxBottom:
        # convert mouse position y to duty cycle from 0 <- dc <- 100
        pwm_dutyCycle = (1 - ((pwm_dutyCycle - boxTop) / (boxBottom - boxTop)))
        pwm_dutyCycle = int(100 * pwm_dutyCycle)
        pwmToSpeaker.ChangeDutyCycle(pwm_dutyCycle)
        pwmToLED.ChangeDutyCycle(pwm_dutyCycle)
        pwm_dc_label.config(text="PWM Duty Cycle=" + str(pwm_dutyCycle))
        pwm_dc_label.update_idletasks()


master.bind('<Motion>', motion)
master.mainloop()
