# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class ScrapyWorkuaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PersonItem(Item):

    name = Field(null=True)
    age = Field(null=True)
    place = Field(null=True)
    detail_info = Field(null=True)

