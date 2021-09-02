#! /usr/bin/ensv python
# -*- coding: UTF-8 -*-
# this is for the "—" in the land strings, TODO: move strings to a file
from __future__ import print_function
from enum import Enum
import Bin
import Cam
import MCard
# import GPIO_Manger
import pickle


class State(Enum):
    STOPPED = 0
    PAUSED = 1
    RUNNING = 2
    ERROR = 3
    FULL = 4
    EMPTY = 5


class Config:
    def __init__(self):
        global config
        self._relay_control = relay_control
        print(sys.version_info[0])
        # ConfigParser changed to configparser in python 3
        if sys.version_info[0] >= 3:
            python3 = True
            import configparser  # 3
            config = configparser.ConfigParser()  # 3
        else:
            python3 = False
            import ConfigParser  # 2
            config = ConfigParser.ConfigParser()  # 2
        config.read('/home/carter/relay/PySockets/server.confg')


class Mode:
    def __init__(self):
        self.state = State.STOPPED
        self.mode_num = None
        self.metrics = None
        self.bins = [Bin.Bin(x) for x in range(12)]  # make bins 0-9

    def __del__(self):
        pass

    def change_mode(self, new_mode):
        self.mode_num = new_mode
        self.metrics = None
        self.state = State.RUNNING

    # inform the GPIO manger to update light and stop the servo and what not

    def load_modes(self):
        pass  # read the spreadsheet

    def test(self):
        self.mode_num = 1
        cn = Cam.CardNumbers()
        prc = Cam.Price()
        mtgsdk_cards = cn.cards
        import random
        for x in range(30):
            randCard = mtgsdk_cards[random.randint(0, len(mtgsdk_cards) - 1)]
            mcard = MCard.MCard(randCard, prc.get(randCard.number))
            # mcard = MCard.MCard(randCard, 0.1) #remove when on a network
            binloc = self.what_bin(mcard)
            print("randCard.number:", randCard.number, "in bin:", binloc)
            if binloc:
                self.bins[binloc - 1].add(mcard)
        print([len(x.cards) for x in self.bins])

        # from IPython import embed
        # embed()
        # import web
        # site = web.Web(nbins=self.bins)
        # site.bins = self.bins
        # site.app.run(host="0.0.0.0", port=9090)
        # card_num = cn.get_card_number(card_name)
        pass

    def run(self):
        print("Running Test")
        self.test()
        print("Done running Test")
        return

        cam = Cam.Cam()
        detect = Cam.Detect()
        cn = Cam.CardNumbers()
        prc = Cam.Price()
        gm = GPIO_Manger()
        pic = '/tmp/current.jpg'
        # TODO: surround with a true loop that will contain the entire
        # state machene
        while self.state == State.RUNNING:
            gm.feed()
            cam.take(pic)
            card_names = detect.detect(pic)
            if card_names:
                card_num = cn.get_card_number(card_names[0])
            # add to bin class, spreadsheet and website
            else:
                card_num = None

            if card_num:
                bin_num = self.what_bin(card_num, prc)
                self.bins[bin_num - 1]
                # TODO: add to bin and sweep to it
                gm.sweepto(bin_num - 1)

    def what_bin(self, mcard):
        # TODO: check the csv for requirements, for now hard code a single mode
        # TODO: Create a wighting system and a parser for sorting requirements
        # TODO use self reference to get the mode and appropriate state from csv
        if not mcard.card or not mcard.value:  # Bin 1:unknown/upside down
            return 1
        if mcard.value > 1:  # Bin 3:above price cutoff ($1)
            return 3
        if mcard.value > .19:  # Bin 2:above price cutoff ($0.19-$1)
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
        if mcard.card.original_type in lands:
            return 12  # Bin 12: land(special)
        elif mcard.card.original_type in basic_lands:
            return 11  # Bin 11: land(basic)

        if len(mcard.card.color_identity) > 1 or len(mcard.card.colors) > 1:
            return 10  # multi color
        if len(mcard.card.color_identity) == 0 or len(mcard.card.colors) == 0:
            return 9  # colorless

        colors = ['Red', 'White', 'Blue', 'Black', 'Green']
        bin_for_color = [4, 5, 6, 7, 8]
        try:
            return bin_for_color[colors.index(mcard.card.colors[0])]
        except ValueError:
            print("ValueError", mcard.card.colors)
            return 1  # unknown color error
        except IndexError:
            print("IndexError", mcard.card.colors)
            return 1  # unknown color error
        '''  # look at contains insted of in, as case is broken on some cards in the api
		types = ['Sorcery', 'Instant', 'Artifact', 'Creature', 'Legendary', 'Land', 'Other' , 'Unknown']
		'''
