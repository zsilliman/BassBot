import RPi.GPIO as GPIO
import time
import threading
import sys
import os
import pygame
import subprocess
import pigpio
import thread

#=================================================#
#                     SETUP                       #
#=================================================#


GPIO.setmode(GPIO.BCM)
#reset hardware PWM
hw_pi = pigpio.pi()
hw_pi.hardware_PWM(13,0,0)
hw_pi.hardware_PWM(12,0,0)
time.sleep(0.5)
hw_pi.stop()

#startup again
hw_pi = pigpio.pi()

#Set values for clockwise and counterclockwise for stepper
CW  = 1
CCW = 0

#Assign GPIO pins to hardware
DIR = 20
STEP= 21
SERV1 = 13
SERV2 = 12
SE1 = 5
SE2 = 19
SE3 = 6
SE4 = 26
AMP = 16
DUCK = 23

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DUCK, GPIO.OUT)
GPIO.setup(SE1, GPIO.OUT)
GPIO.setup(SE2, GPIO.OUT)
GPIO.setup(SE3, GPIO.OUT)
GPIO.setup(SE4, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(SERV1, GPIO.OUT)
GPIO.setup(SERV2, GPIO.OUT)
GPIO.setup(AMP, GPIO.OUT)
GPIO.output(AMP, GPIO.LOW)
GPIO.output(DUCK, GPIO.LOW)

servo1 = GPIO.PWM(SERV1, 50)
servo2 = GPIO.PWM(SERV2, 50)

#fret mappings
fret_map = [0, 0, 0, 200, 400, 600, 775, 950, 1125, 1275, 1400, 1525, 1670]

#Stepper motor step delay and stepper motor location
delay = 0.0004
current_step = 0

#Waiting delay measurements
step_time     = 0.0005
push_delay    = 0.25
release_delay = 0.25
pluck_delay   = 0.2

print("HARDWARE SETUP COMPLETE")

#=================================================#
#                     DUCK                        #
#=================================================#

#Mr Duck celebration
def mrduck():
	for i in range(0, 8):
		GPIO.output(DUCK, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(DUCK, GPIO.LOW)
		time.sleep(0.2)
	GPIO.output(DUCK, GPIO.LOW)


#=================================================#
#                      AMP                        #
#=================================================#

#Turn off the signal to the amplifier
def amp_off():
  GPIO.output(AMP, GPIO.HIGH)

#Turn on the signal to the amplifier
def amp_on():
  GPIO.output(AMP, GPIO.LOW)

#=================================================#
#                    STEPPER                      #
#=================================================#

#Step forward [steps] steps
def step_forward(steps):
	global current_step
	GPIO.output(DIR, CCW)
	for x in range(steps):
		GPIO.output(STEP, GPIO.HIGH)
		time.sleep(delay)
		GPIO.output(STEP, GPIO.LOW)
		time.sleep(delay)
		current_step += 1

#Step backward [steps] steps
def step_backward(steps):
	global current_step
	GPIO.output(DIR, CW)
	for x in range(steps):
		GPIO.output(STEP, GPIO.HIGH)
		time.sleep(delay)
		GPIO.output(STEP, GPIO.LOW)
		time.sleep(delay)
		current_step -= 1

#Abstracted function to go to a desired location,
#knowing the current location
def go_to(dest):
	global current_step
	#Create 1D vector to new position
	diff = dest-current_step
	#Step in that direction
	if (diff < 0):
		step_backward(-diff)
	else:
		step_forward(diff)


#=================================================#
#             SERVO FRETTING DEVICE               #
#=================================================#

# NOTE: Freq=Hz and duty=10,000*% (25%=250,000)

#Function to clamp frets using hardware PWM. Also turns off amp
def push_HW():
	amp_off()
	hw_pi.hardware_PWM(SERV1, 50, 50000)
	hw_pi.hardware_PWM(SERV2, 50, 100000)
	time.sleep(push_delay)
	amp_on()

#Function to release frets using hardware PWM. Also turns off amp
def release_HW():
	amp_off()
	hw_pi.hardware_PWM(SERV1, 50, 110000)
	hw_pi.hardware_PWM(SERV2, 50, 40000)
	time.sleep(release_delay)
	amp_on()

#unused software PWM GPIO controllers
servo1.start(0)
servo2.start(0)

#Unused software PWM fretting servo control
def push():
  global servo1, servo2
  servo1.ChangeFrequency(50) #0.75==>46.5, 1.5==>48.2, 2.25==>44.9
  servo1.ChangeDutyCycle(8)
  servo2.ChangeFrequency(50)
  servo2.ChangeDutyCycle(6.2)
  time.sleep(push_delay)

#Unused software PWM fretting servo control
def release():
  global servo1, servo2
  servo1.ChangeFrequency(50)
  servo1.ChangeDutyCycle(11)
  servo2.ChangeFrequency(50)
  servo2.ChangeDutyCycle(3)
  time.sleep(release_delay)
  servo1.ChangeDutyCycle(0)
  servo2.ChangeDutyCycle(0)

def servo_stop():
  global servo1, servo2
  servo1.ChangeDutyCycle(0)
  servo2.ChangeDutyCycle(0)
  servo1.stop()
  servo2.stop()

#=================================================#
#                 PLUCKING SERVOS                 #
#=================================================#

#class used to control the plucking mechanism.
#Each instance represents one motor/pick
class PickController:
	LEFT = 1
	UNKNOWN = 0
	RIGHT = -1
	def __init__(self, pin, Hz, left, right):
		self.p =GPIO.PWM(pin, 50)
		self.p.start(0)
		self.position = PickController.UNKNOWN #-1=RIGHT, 0=???, 1=LEFT
		self.left = left
		self.right = right

	def pluck_left(self):
		self.position = PickController.UNKNOWN
		self.p.ChangeDutyCycle(self.left)
		time.sleep(0.2)
		self.p.ChangeDutyCycle(0)
		time.sleep(0.8)
		self.position = PickController.LEFT

	def pluck_right(self):
		self.position = PickController.UNKNOWN
		self.p.ChangeDutyCycle(self.right)
		time.sleep(0.2)
		self.p.ChangeDutyCycle(0)
		time.sleep(0.8)
		self.position = PickController.RIGHT

	#useful method to pluck string in either direction
	def pluck(self):
		if self.position == PickController.LEFT:
			self.pluck_right()
		else:
			self.pluck_left()

	def stop(self):
		self.p.ChangeDutyCycle(0)
		self.p.stop()

#Create pick controller object for each pick
pick0 = PickController(SE1, 50, 3.4, 5.2)
pick1 = PickController(SE2, 50, 4.1, 5.8)
pick2 = PickController(SE3, 50, 5, 6.7)
pick3 = PickController(SE4, 50, 6.6, 8.6)

picks = [pick0, pick1, pick2, pick3]


#=================================================#
#               ABSTRACTED FUNCS                  #
#=================================================#

#Compute approximate time to perform the action of playing a given note
def compute_transition_time(fret, string):
	global current_step
	dest = fret_map[fret]
	diff = dest - current_step
	if (abs(diff) <= 5):
		return pluck_delay
	return diff * step_time + pluck_delay + push_delay + release_delay

#Abstracted function to play a given note
def play_fret(fret, string, ring_time=0, callback=None, release=True):
	#No need to move stepper or push solenoid for open string
	if (fret != 0 and release == True):
		go_to(fret_map[fret])
		push_HW()
	picks[string].pluck()
	if (ring_time > 0):
		time.sleep(ring_time)
	#Only need to release solenoid for fretted strings
	if (fret != 0 and release == True):
		release_HW()
	if (callback is not None):
		callback()

#Cleanup all hardware related resources
def clean():
        release_HW()
	hw_pi.stop()
	GPIO.output(DUCK, GPIO.LOW)
	for pick in picks:
		pick.stop()
	go_to(0)
	servo_stop()
	servo1.stop()
	servo2.stop()
	GPIO.cleanup()
	print("hardware cleanup done.")

#Unused function to play note in a new thread to prevent GUI freeze
def play_fret_async(fret, string, ring_time=0, callback=None):
	my_thread = threading.Thread(target=play_fret, args=(fret, string, ring_time, callback))
	my_thread.start()

#Method used to reset the locations of the picks to a known position
def setup_picks():
	global picks
	amp_off()
	for pick in picks:
		pick.pluck()
	amp_on()

#Useful function for testing and tuning PWM duty cycles for the picks
def tune_pick(index):
	global picks
	while(True):
		picks[index].pluck()
		#picks[(index+1)%4].pluck()


#=================================================#
#                GPIO QUIT BUTTON                 #
#=================================================#

running = True

#Running status function used in other files to help terminate the program
def is_running():
	global running
	return running

#Callback function for quit button
def quit_button(channel):
	print("exiting...")
	global running
	running = False

#Event listener for quit button
GPIO.add_event_detect(27, GPIO.FALLING, callback=quit_button, bouncetime = 2000)

#=================================================#
#             MAIN LOOP FOR TESTING               #
#=================================================#


setup_picks()