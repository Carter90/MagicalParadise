#! /usr/bin/env python
from __future__ import print_function


class MCard:
    def __init__(self, mtgsdk, tcgplayer=0.0):
        self.card = mtgsdk
        self.value = tcgplayer


'''
card:
	all(), artist, border, cmc, color_identity, colors, find(), flavor, foreign_names, hand, id, image_url, layout, legalities, life, loyalty, mana_cost, multiverse_id, name, names, number, original_text, original_type, power, printings, rarity, release_date, RESOURCE, rulings, set, set_name, source, starter, subtypes, supertypes, text, timeshifted, toughness, type, types, variations, watermark, where()

value: double
'''
