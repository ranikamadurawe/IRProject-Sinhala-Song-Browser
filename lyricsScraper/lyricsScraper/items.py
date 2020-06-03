# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class LyricsscraperItem(Item):
    artist = Field()
    writer = Field()
    composer = Field()
    releaseDate = Field()
    genre = Field()
    songLyrics = Field()
    tags = Field()
    title = Field()
    movie = Field()
    url = Field()
    views = Field()
    key = Field()
    beat = Field()
