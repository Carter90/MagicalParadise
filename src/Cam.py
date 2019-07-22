#! /usr/bin/env python
from __future__ import print_function
from picamera import PiCamera
from time import sleep
from PIL import Image
import pytesseract
import cv2
import sys
import requests
import difflib
from mtgsdk import Card
import string
import pickle


class Cam: 
	def __init__(self): 
		print('Camera Starting') 
		self.camera = PiCamera()
		self.camera.start_preview()
		sleep(2.5)
		print('Camera Ready') 

	def __del__(self): 
		self.camera.stop_preview()
		print('Camera Stopped')
	
	def take(self, filename='/tmp/image.jpg'):
		# ram disk is the safest on the sd card
		self.camera.capture(filename)


# http://trainyourtesseract.com/
class Detect:
	def __init__(self, nspell=None):
		if nspell:
			self.spell = nspell
		else:
			self.spell = Spell()
	''' returns none if no valid card was detected'''
	def detect(self, filename='/tmp/current.jpg',debug=False):
		pic = cv2.imread(filename)
		gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)  # convert to grayscale
		cropped = gray[50:100, 55:550]  # read and crop
		# crop for the bottom if upside down

		if debug:  # show the output images
			cv2.imshow('Gray:', gray)
			cv2.imshow('Cropped:', cropped)
			cv2.waitKey(0)
		# TODO: mana coverup mask use the waldo stratgy
		# TODO: remove mana https://stackoverflow.com/questions/17566752/how-to-find-subimage-using-the-pil-library
		# cv2.bitwise_and
		# https://machinelearningmastery.com/using-opencv-python-and-template-matching-to-play-wheres-waldo/
		# invert this mask and we are good

		# load the image as a PIL/Pillow image, apply OCR
		text = pytesseract.image_to_string(Image.fromarray(cropped))
		# lang="Belerenn", config='--tessdata-dir "./tessdata"') #addition args
		print(text)

		# if text is a valid name or close enough return else do the rotation
		possible_matches = self.spell.check(text)
		if possible_matches:
			print('Matches:', possible_matches)
			return possible_matches
		else:  # if no valid text is detected on top rotate 180 and look again
			(h, w) = pic.shape[:2]
			center = (w / 2, h / 2)  # int division needed
			rotated = cv2.warpAffine(pic, cv2.getRotationMatrix2D(center, 180, 1.0), (w, h))
			cropped = rotated[50:100, 55:550]
			text = pytesseract.image_to_string(Image.fromarray(cropped))
			print(text)
			possible_matches = self.spell.check(text)
			if possible_matches:
				print('Matches:', possible_matches)
				return possible_matches
		return None  # no detections rotated or otherwise


class Price:
	def __init__(self):
		with open("../cfg/tcgplayer.token", "r") as tokenFile:
			# TODO: test with tokenFile.readline().strip()
			self.token = tokenFile.readlines()[0].strip()
		self.headers = {'Accept': 'application/json', 'Authorization': 'bearer' + self.token}

	def get(self, product_id):
		price_url = "http://api.tcgplayer.com/pricing/product/{0}".format(product_id)
		response = requests.get(price_url, headers=self.headers)
		return response.json()['results'][0]['marketPrice']


class Spell:
	def __init__(self, cards_filename='cardnames.txt'):
		# NOTE: cpython garbage collector handles cardsFileName file instance
		self.card_names = set(cardname.strip() for cardname in open(cards_filename))

	def check(self, check_me=''):
		return difflib.get_close_matches(check_me, self.card_names)

	def update(self, filename='cardnames.txt'):
		"""This will take a long time like 20+ mins"""
		cards = Card.all()
		# get a set of all the  card names lower case
		cs = {card.name.lower() for card in cards}
		self.card_names = cs  # save to current instance
		with open(filename, 'w') as fi:
			for a_card_name in cs:
				fi.write("%s\n" % a_card_name)
		pickle.dump(cards, open("cards.p", "wb"))  # dump all the cards
		# get all the card pricing?
		# long call to get all the card instances


class CardNumbers:
	def __init__(self, cards_pickle='cards.p'):
		self.cards = pickle.load(open(cards_pickle, "rb"))
		self.cardNameNumDict = {card.name: card.number for card in self.cards}
		
	def get_card_number(self, name):
		return self.cardNameNumDict[name]
	

if __name__ == "__main__":
	cam = Cam() 
	pict = '/tmp/current.jpg'
	cam.take(pict)
	detect = Detect()
	card_name = detect.detect(pict)[0]
	cn = CardNumbers()
	card_num = cn.get_card_number(card_name)
	Price().get(card_num)
