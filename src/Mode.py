#! /usr/bin/env python
from __future__ import print_function
from enum import Enum
import Bin
import Cam
import GPIO_Manger

class State(Enum):
	STOPPED=0
	PAUSED=1
	RUNNING=2
	ERROR=3
	FULL=4
	EMPTY=5

class Mode:
	def __init__(self):
		self.state=State.STOPPED
		self.mode_num = None
		self.metrics = None
		self.bins = [ Bin.Bin(x) for x in range(10) ] #make bins 0-9
		
	def __del__(self):
		pass
	
	def change_mode(self, new_mode):
		self.mode_num = new_mode
		self.metrics = None
		self.state=State.RUNNING
		
		#inform the GPIO manger to update light and stop the servo and what not
		
	def load_modes():
		pass #read the spreadsheet
	
	def run(self):
		cam = Cam() 
		detect = Detect()
		cn = CardNumbers()
		gm = GPIO_Manger()
		pic='/tmp/current.jpg'
		
		while self.state == State.RUNNING:
			gm.feed()
			cam.take(pic)
			cardnames = detect.detect(pic)
			if cardnames:
				cardnum = cn.get_card_number(cardname)
				#add to bin class, spredsheet and website
			else: 
				cardnum = None
			gm.sweepto(what_bin(cardnum))
	
	def what_bin(self, card):
		#TODO: check the csv for requirements, for now hardcode a mode
		if self.mode_num == 1:
			if not card:  #Bin 1	unknown/backward
				return(1)
			price = Price().get(cardnum)
			if price > 1: #Bin 3	above price cutoff ($1)
				return(3)
			if price > .19: #Bin 2	above price cutoff ($0.19-$1)
				return(2)
			
			basic_lands={'Basic Land — Forest', 'Basic Land — Island', 'Basic Land — Mountain', 'Basic Land — Plains', 'Basic Land — Swamp'}
			lands={ 'Basic Snow Land — Forest', 'Basic Snow Land — Island', 'Basic Snow Land — Mountain', 'Basic Snow Land — Plains',
 'Basic Snow Land — Swamp', 'Land', 'Land — Desert', 'Land — Forest Island', 'Land — Forest Plains',
 'Land — Island Mountain', 'Land — Island Swamp', 'Land — Lair', 'Land — Mountain Forest',
 'Land — Mountain Plains', 'Land — Plains Island', 'Land — Plains Swamp',
 'Land — Swamp Forest', 'Land — Swamp Mountain', 'Land — Urza’s Mine',
 'Land — Urza’s Power-Plant', 'Land — Urza’s Tower'}
			if card.type in card.original_type == 'Land':
				if basic_lands:#Bin 11	land(basic)
				else if #Bin 12	land(special)
				
			if len(card.color_identity) > 1: 
				return(10) #multi color
			if len(card.color_identity) == 0: 
				return(9) #colorless
			if 'Red' in card.colors:
				return(4)
			if 'White' in card.colors:
				return(5)
			if 'Blue' in card.colors:
				return(6)
			if 'Black' in card.colors:
				return(7)
			if 'Green' in card.colors:
				return(8)

