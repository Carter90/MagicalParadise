import RPi.GPIO as GPIO
from time import sleep

class GPIO_Manger: 
	_bins = [2.5, 7.5, 12.5] #bin positions for servo  #0, 90, 180 degree
	_statelights = [17, 27, 22]
	_modelights = [25, 12, 16, 20]
	_modebuttons = [ 5, 13, 19, 26, 23 ]
	_buttonNames = ["Pause/UnPause button", "Mode button 1", "Mode button 2", "Mode button 3", "Mode button 4"]
	_servopin = 6
	def __init__(self): 
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self._servopin, GPIO.OUT)
		self.servo = GPIO.PWM(self._servopin, 50)
		self.servo.start(self._bins[0])
		GPIO.setup(self._statelights, GPIO.OUT)
		GPIO.setup(self._modelights, GPIO.OUT)
		GPIO.setup(self._modebuttons, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		for pin in self._modebuttons:  # set button pins to 3.3v
			#GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #PUD_DOWN or PUD_UP
			GPIO.add_event_detect(pin, GPIO.RISING, callback=self.button_pressed, bouncetime=1500) #was GPIO.FALLING
	
	def __del__(self): 
		GPIO.cleanup()
		print('GPIO cleaned up')
	
	#moves the servo to the bin
	def sweepto(self, bin_num=0): 
		self.servo.ChangeDutyCycle(self._bins[bin_num]) 
	
	#TODO: Feed till optical switch is tripped then return
	def feed(self):
		pass
		
	#TODO: open solenoid, delay for card to drop, release solenoid
	def drop_card(self):
		pass
	
	def button_pressed(self, channel):
		print("Button Pressed", self._buttonNames[self._modebuttons.index(channel)])
	
	def test_loop(self):
		while True: 
			for x in range(3):
				self.sweepto(x)
				sleep(.5)
			for pin in self._statelights + self._modelights:
				GPIO.output(pin,GPIO.HIGH) # on
				sleep(.2)
			for pin in self._statelights + self._modelights:
				GPIO.output(pin,GPIO.LOW) #off
				sleep(.2)
				
if __name__ == "__main__":
	gm = GPIO_Manger()
	gm.test_loop()

