#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# this is for the "—" in the land strings, TODO: move strings to a file
from __future__ import print_function
from enum import Enum
import Bin
import Cam
import GPIO_Manger


class State(Enum):
	STOPPED = 0
	PAUSED = 1
	RUNNING = 2
	ERROR = 3
	FULL = 4
	EMPTY = 5


class Mode:
	def __init__(self):
		self.state = State.STOPPED
		self.mode_num = None
		self.metrics = None
		self.bins = [Bin.Bin(x) for x in range(10)]  # make bins 0-9
		
	def __del__(self):
		pass
	
	def change_mode(self, new_mode):
		self.mode_num = new_mode
		self.metrics = None
		self.state = State.RUNNING
		
		# inform the GPIO manger to update light and stop the servo and what not
		
	def load_modes(self):
		pass  # read the spreadsheet
	
	def run(self):
		cam = Cam.Cam()
		detect = Cam.Detect()
		cn = Cam.CardNumbers()
		pr = Cam.Price()
		gm = GPIO_Manger()
		pic = '/tmp/current.jpg'
		
		while self.state == State.RUNNING:
			gm.feed()
			cam.take(pic)
			card_names = detect.detect(pic)
			if card_names:
				card_num = cn.get_card_number(card_names[0])
				# add to bin class, spreadsheet and website
			else: 
				card_num = None
			gm.sweepto(self.what_bin(card_num, pr))
	
	def what_bin(self, card, pricec):
		# TODO: check the csv for requirements, for now hard code a single mode
		# TODO use self reference to get the mode and appropriate state from csv
		if self.mode_num == 1:
			if not card:  # Bin 1:unknown/backward
				return 1
			price = pricec.get(card)
			if price > 1:  # Bin 3:above price cutoff ($1)
				return 3
			if price > .19:  # Bin 2:above price cutoff ($0.19-$1)
				return 2
			
			basic_lands = {'Basic Land — Forest', 'Basic Land — Island',
						 'Basic Land — Mountain', 'Basic Land — Plains',
						 'Basic Land — Swamp'}
			lands = {'Basic Snow Land — Forest', 'Basic Snow Land — Island',
					'Basic Snow Land — Mountain', 'Basic Snow Land — Plains',
					'Basic Snow Land — Swamp', 'Land', 'Land — Desert',
					'Land — Forest Island', 'Land — Forest Plains',
					'Land — Island Mountain', 'Land — Island Swamp',
					'Land — Lair', 'Land — Mountain Forest',
					'Land — Mountain Plains', 'Land — Plains Island',
					'Land — Plains Swamp', 'Land — Swamp Forest',
					'Land — Swamp Mountain', 'Land — Urza’s Mine',
					'Land — Urza’s Power-Plant', 'Land — Urza’s Tower'}

			if card.original_type in lands:
				return 12  # Bin 12: land(special)
			elif card.original_type in basic_lands:
				return 11  # Bin 11: land(basic)

			if len(card.color_identity) > 1: 
				return 10  # multi color
			if len(card.color_identity) == 0: 
				return 9  # colorless
			if 'Red' in card.colors:
				return 4
			if 'White' in card.colors:
				return 5
			if 'Blue' in card.colors:
				return 6
			if 'Black' in card.colors:
				return 7
			if 'Green' in card.colors:
				return 8
