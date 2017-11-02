# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FantacalcioItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PlayerItem(scrapy.Item):
    nome = scrapy.Field()
    numero = scrapy.Field()
    ruolo = scrapy.Field()
    squadra = scrapy.Field()
    stagione = scrapy.Field()
    giornata = scrapy.Field()
    voto = scrapy.Field()
    gol = scrapy.Field()
    assist = scrapy.Field()
    rigore = scrapy.Field()
    rigore_sbagliato = scrapy.Field()
    autogol = scrapy.Field()
    ammonizione = scrapy.Field()
    espulsione = scrapy.Field()
    fantavoto = scrapy.Field()
