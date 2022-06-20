import scrapy
import json
from scrapy import Request
import pandas as pd
from itemadapter import ItemAdapter
from ..items import WebscrapingItem

class WebscrapingSpider(scrapy.Spider):
  name = 'webScraping'

  def start_requests(self):
      #calling Dawn Categories
      yield Request('https://www.dawn.com/business',callback=self.Dawn, meta={'category': 'business','source': 'DAWN'})
      yield Request('https://www.dawn.com/sport',callback=self.Dawn, meta={'category': 'sports','source': 'DAWN'})
      yield Request('https://www.dawn.com/tech',callback=self.Dawn, meta={'category': 'tech','source': 'DAWN'})

      #calling Tribune Categories
      yield Request('https://tribune.com.pk/Business',callback=self.TribuneBusiness, meta={'category': 'business','source': 'Tribune' })
      yield Request('https://tribune.com.pk/Sports',callback=self.Tribune, meta={'category': 'sports','source': 'Tribune' })
      yield Request('https://tribune.com.pk/Technology',callback=self.Tribune, meta={'category': 'tech','source': 'Tribune' })

  def Dawn(self,response):
    for newsLink in response.css("h2.story__title a::attr(href)"):
      yield response.follow(newsLink.get(), callback=self.parseDawn, meta={'category': response.meta['category'],'source': response.meta['source']})

  def TribuneBusiness(self,response):
      for all_news_link in response.css('ul.listing-page li div.row div.col-md-8 div.horiz-news3-caption a::attr(href)'):
        yield response.follow(all_news_link.get(), callback=self.parseTribuneBusiness, meta={'category': response.meta['category'],'source': response.meta['source']})

  def Tribune(self,response):
      for all_news_link in response.css('ul.listing-page li div.row div.col-md-8 div.horiz-news3-caption a::attr(href)'):
        yield response.follow(all_news_link.get(), callback=self.parseTribune, meta={'category': response.meta['category'],'source': response.meta['source']})            

  def parseDawn(self, response):
    items = WebscrapingItem()

    items['title'] = response.css("h2.story__title a.story__link::text").extract_first().strip() ,
    items["author"] = response.css("span.story__byline a.story__byline__link::text").extract_first() ,
    items['content'] = response.css("p::text").extract(),
    items["image"] = response.css("figure.media--uneven div.media__item  picture img::attr(src)")[0].extract(),
    items['time'] = response.css("span.story__time span.timestamp--time span.timestamp__time::text").extract(), 
    items["date"] = response.css("span.story__time span.timestamp--date::text").extract()  
    category = response.meta['category']
    source = response.meta['source']

    items = {
      'title' : self.filterAttr(items['title']), 
      "author": self.filterAttr(items['author']),
      "content": self.filterTuple(items['content']),
      "image": self.filterAttr(items['image']),
      "time": self.filterTuple(items['time']),
      "date": self.filterAttr(items['date']),
      "category": category,
      "source": source
    }

    yield items

  def parseTribuneBusiness(self, response):
    items = WebscrapingItem()

    items['title'] = response.css('div.story-box-section h1::text').get()
    items["author"] = response.css('div.story-box-section span.storypage-leftside div.left-authorbox span a::text').get()
    items['content'] = response.css('p > span:nth-child(1)::text , p:nth-child(3)::text , .location-names::text').extract()
    items["image"] = response.css('div.story-box-section div.mainstorycontent-parent div.storypage-main-section2 div.storypage-rightside span.top-big-img div.story-featuredimage div.amp-top-main-img div.featured-image-global img::attr(src)').get()
    items["date"] = response.css('div.story-box-section span.storypage-leftside div.left-authorbox span::text')[1].get()
    time = response.xpath('//script[@type="application/ld+json"]/text()').get()
    json_data = json.loads(time, strict=False)
    category = response.meta['category']
    source = response.meta['source']

    items = {
    'title' : self.filterAttr(items['title']), 
    "author": self.filterAttr(items['author']),
    "content": self.filterAttr(items['content']),
    "image": self.filterAttr(items['image']),
    "time":json_data['datePublished'],
    "date": self.filterAttr(items['date']),
    "category": category,
    "source": source
  }
    
    yield items

  def parseTribune(self, response):
    items = WebscrapingItem()

    items['title'] = response.css('div.story-box-section h1::text').get()
    items["author"] = response.css('div.story-box-section span.storypage-leftside div.left-authorbox span a::text').get()
    items['content'] = response.css('.story-text p::text').extract()
    items["image"] = response.css('div.story-box-section div.mainstorycontent-parent div.storypage-main-section2 div.storypage-rightside span.top-big-img div.story-featuredimage div.amp-top-main-img div.featured-image-global img::attr(src)').get()
    items["date"] = response.css('div.story-box-section span.storypage-leftside div.left-authorbox span::text')[1].get()
    time = response.xpath('//script[@type="application/ld+json"]/text()').get()
    json_data = json.loads(time, strict=False)
    category = response.meta['category']
    source = response.meta['source']

    items = {
      'title' : self.filterAttr(items['title']), 
      "author": self.filterAttr(items['author']),
      "content": self.filterAttr(items['content']),
      "image": self.filterAttr(items['image']),
      "time":json_data['datePublished'],
      "date": self.filterAttr(items['date']),
      "category": category,
      "source": source
    }

    yield items  

  def filterAttr(self, attr):
    return "".join(attr)

  def filterTuple(self, attr):
    listAttr = list(attr)
    return " ".join([' '.join([str(c) for c in lst]) for lst in listAttr])
    
