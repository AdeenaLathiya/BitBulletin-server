# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# from turtle import title
import scrapy
from itemadapter import ItemAdapter

class WebscrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    image = scrapy.Field()
    time = scrapy.Field()
    # date = scrapy.Field()
    category = scrapy.Field()
    source = scrapy.Field()
    summary = scrapy.Field()
    link = scrapy.Field()

    pass
