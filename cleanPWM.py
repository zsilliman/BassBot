import RPi.GPIO as GPIO
import time
import threading
import sys
import subprocess
import pigpio

GPIO.setmode(GPIO.BCM)
hw_pi = pigpio.pi()

hw_pi.hardware_PWM(13,0,0)
hw_pi.hardware_PWM(12,0,0)

time.sleep(1)
hw_pi.stop()
GPIO.cleanup()
print("done")
