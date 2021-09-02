#! /usr/bin/env python
from __future__ import print_function
import datetime
import csv
import io
import os.path
import pickle
from os import path


class Bin:
    def __init__(self, bin_num=0):
        self.cap = 500
        self.cards = list()
        self.bin_num = bin_num
        self.now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        self.file = "/tmp/magic/" + self.now + '.' + str(self.bin_num)
        self.csv = self.file + ".csv"
        self.header = ['Name', 'Number', 'Price']

    def load(self, filename):
        # TODO: this is to load a past bin to continue where it left off
        # pickle??
        pass

    def dump(self):
        pickle.dump(self.cards, open("bin" + self.file + ".p", "wb"))

    def num_cards(self):
        return len(self.cards)

    def add(self, card):
        print("Adding: ", card.card.name)
        self.cards.append(card)
        '''row = [card.card.name,card.card.number,card.value]
        file_exists = path.isfile(self.file)
        with open(self.csv, 'a') as csvFile:
            writer = csv.writer(csvFile) 
            #if not file exists
            #TODO: check if the file exists if it does then dont add header
            if not file_exists:
                writer.writerow(self.header)  # saves the header to a csv file
            writer.writerow(row)  # saves the card to a csv file
        '''
        return
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
