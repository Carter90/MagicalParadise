#! /usr/bin/env python
from __future__ import print_function
import datetime
import csv 
import io


class Bin:
	def __init__(self,binNum):
		self.cap = 500
		self.cards = list() 
		self.bin_num = binNum
		self.now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
	
	def num_cards(self):
		return len(self.cards)
	
	def add(self, card):
		self.cards.append(card)
		row = [11, card, 'price']
		with open(self.now+'.'+str(self.bin_num)+'.csv', 'a') as csvFile:
			writer = csv.writer(csvFile) 
			writer.writerow(row)  # saves the card to a csv file
		# TODO: handle a failure state
	
	def in_bin(self, card):
		# { card.card.name.lower() for card in cards }
		return card in self.cards

	def empty(self):
		""" empties the bin and will save it with a reference string"""
		self.cards = list()
		self.now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
	
	def full(self):
		return len(self.cards) == self.cap