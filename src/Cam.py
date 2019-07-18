#! /usr/bin/env python
from __future__ import print_function
#from picamera import PiCamera
from time import sleep
from PIL import Image
import pytesseract
import cv2
import sys

class Cam: 
	def __init__(self): 
		print('Camera Starting') 
		self.camera = PiCamera()
		self.camera.start_preview()
		sleep(2.5)
		print('Camera Ready') 

	def __del__(self): 
		camera.stop_preview()
		print('Camera Stopped')
	
	def take(self, filename='/tmp/image.jpg'):
		#ram disk is the safest on the sd card
		camera.capture(filename) 

#http://trainyourtesseract.com/
class Detect:
	def __init__(self, nspell=None):
		if nspell:
			self.spell = nspell
		else:
			self.spell = Spell()
	''' returns none if no valid card was detected'''
	def detect(filename='/tmp/current.jpg',debug=False):
		pic = cv2.imread(filename)
		gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY) #convert to grayscale
		cropped = gray[50:100, 55:550] #read and crop
		#crop for the bottom if upside down

		if debug:# show the output images
			cv2.imshow('Gray:', gray)
			cv2.imshow('Cropped:', cropped)
			cv2.waitKey(0)
		# TODO: mana coverup mask use the waldo stratgy
		#TODO: remove mana https://stackoverflow.com/questions/17566752/how-to-find-subimage-using-the-pil-library
		#cv2.bitwise_and
		#https://machinelearningmastery.com/using-opencv-python-and-template-matching-to-play-wheres-waldo/ invert this mask and we are in bussness

		# load the image as a PIL/Pillow image, apply OCR
		text = pytesseract.image_to_string(Image.fromarray(cropped))#, lang="Belerenn", config='--tessdata-dir "./tessdata"') #,
		print(text)

		#if text is a valid name or close enough return else do the rotation
		posible_matches = self.spell.check(checkme=text)
		if posible_matches:
			print('Matches:', matches)
			return(posible_matches)
		else: #if no valid text is detected on top rotate and look again
			(h, w) = pic.shape[:2]
			center = (w / 2, h / 2) #int division needed
			rotated = cv2.warpAffine(pic, cv2.getRotationMatrix2D(center, 180, 1.0), (w, h))
			cropped = rotated[50:100, 55:550]
			text = pytesseract.image_to_string(Image.fromarray(cropped))
			print(text)
			posible_matches = self.spell.check(checkme=text)
			if posible_matches:
				print('Matches:', matches)
				return(posible_matches)
		return(None) #no detections rotated or otherwise

class Price():
	import requests
	def get(productId):
		with open("../cfg/tcgplayer.token","r") as tokenFile:
			token=tokenFile.readlines()[0].strip()
		headers = {'Accept': 'application/json','Authorization':'bearer'+token}
		price_url = "http://api.tcgplayer.com/pricing/product/{0}".format(productId)
		response = requests.get(price_url,headers=headers)
		data = response.json()
		self.marketPrice=data['results'][0]['marketPrice']
		print(self.marketPrice)

class Spell():
	def __init__(self, cardsFileName='cardnames.txt'):
		import difflib
		# NOTE: cpython will garbage collect the open cardsFileName file instance thus closing it 
		self.cardnames = set(cardname.strip() for cardname in open(cardsFileName))
	def check(checkme = ''):
		return(difflib.get_close_matches(checkme, self.cardnames))

	'''This will take a long time like 20+ mins'''
	def update(filename='cardnames.txt'):
		from mtgsdk import Card
		import string
		c = Card.all()
		#get a set of all the  card names lower case
		cs = { card.name.lower() for card in cards } 
		
		with open(filename, 'w') as fi:
			for cardname in cs:
				fi.write("%s\n" % cardname)
		pickle.dump( c, open( "cards.p", "wb" ) ) #dump all the cards
		#get all the card priceing?
		pass #long call to get all the card instances 

class CardNumbers():
	def __init__(self, cardsPickle='cards.p'):
		self.cards = pickle.load( open( cardsPickle, "rb" ) )
		self.cardnameNumDict = { card.name:card.number for card in self.cards }
		
	def get_card_number(name):
		return self.cardnameNumDict[name]
	

if __name__ == "__main__":
	cam = Cam() 
	pic='/tmp/current.jpg'
	cam.take(pic)
	detect = Detect()
	cardname = detect.detect(pic)[0]
	cn = CardNumbers()
	cardnum = cn.get_card_number(cardname)
	Price().get(cardnum)

