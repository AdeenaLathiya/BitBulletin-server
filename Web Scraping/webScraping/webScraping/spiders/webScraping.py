import scrapy
from scrapy import Request
from ..items import WebscrapingItem

class WebscrapingSpider(scrapy.Spider):
  name = 'webScraping'

  def start_requests(self):
      #calling Dawn Categories
      yield Request('https://www.dawn.com/business',callback=self.DawnBusiness)
      yield Request('https://www.dawn.com/sport',callback=self.DawnSports)
      yield Request('https://www.dawn.com/tech',callback=self.DawnTech)

      #calling Tribune Categories
      yield Request('https://tribune.com.pk/Business',callback=self.TribuneBusiness)
      yield Request('https://tribune.com.pk/Sports',callback=self.TribuneSports)
      yield Request('https://tribune.com.pk/Technology',callback=self.TribuneTech)

  def DawnBusiness(self,response):
    for newsLink in response.css("h2.story__title a::attr(href)"):
      yield response.follow(newsLink.get(), callback=self.parseDawnBusiness)

  def DawnSports(self,response):
      for newsLink in response.css("h2.story__title a::attr(href)"):
        yield response.follow(newsLink.get(), callback=self.parseDawnSports)

  def DawnTech(self,response):
      for newsLink in response.css("h2.story__title a::attr(href)"):
        yield response.follow(newsLink.get(), callback=self.parseDawnTech)

  def TribuneBusiness(self,response):
      for all_news_link in response.css('ul.listing-page li div.row div.col-md-8 div.horiz-news3-caption a::attr(href)'):
        yield response.follow(all_news_link.get(), callback=self.parseTribuneBusiness)

  def TribuneSports(self,response):
      for all_news_link in response.css('ul.listing-page li div.row div.col-md-8 div.horiz-news3-caption a::attr(href)'):
        yield response.follow(all_news_link.get(), callback=self.parseTribuneSports)

  def TribuneTech(self,response):
      for all_news_link in response.css('ul.listing-page li div.row div.col-md-8 div.horiz-news3-caption a::attr(href)'):
        yield response.follow(all_news_link.get(), callback=self.parseTribuneTech)            



  def parseDawnBusiness(self, response):
    items = WebscrapingItem()

    title = response.css("h2.story__title a.story__link::text").extract_first().strip() ,
    author = response.css("span.story__byline a.story__byline__link::text").extract_first() ,
    content = response.css("p::text").extract(),
    image = response.css("figure.media--uneven div.media__item  picture img::attr(src)").extract(),
    time = response.css("span.story__time span.timestamp--time span.timestamp__time::text").extract(), 
    date = response.css("span.story__time span.timestamp--date::text").extract()  
    category = 'business'
    source = 'DAWN'

    items['title'] = title
    items['author'] = author
    items['content'] = content
    items['image'] = image
    items['time'] = time
    items['date'] = date
    items['category'] = category
    items['source'] = source

    yield items

  def parseDawnSports(self, response):
    items = WebscrapingItem()

    title = response.css("h2.story__title a.story__link::text").extract_first().strip() ,
    author = response.css("span.story__byline a.story__byline__link::text").extract_first() ,
    content = response.css("p::text").extract(),
    image = response.css("figure.media--uneven div.media__item  picture img::attr(src)").extract(),
    time = response.css("span.story__time span.timestamp--time span.timestamp__time::text").extract(), 
    date = response.css("span.story__time span.timestamp--date::text").extract() 
    category = 'sports'
    source = 'DAWN'

    items['title'] = title
    items['author'] = author
    items['content'] = content
    items['image'] = image
    items['time'] = time
    items['date'] = date
    items['category'] = category
    items['source'] = source

    yield items

  def parseDawnTech(self, response):
    items = WebscrapingItem()

    title = response.css("h2.story__title a.story__link::text").extract_first().strip() ,
    author = response.css("span.story__byline a.story__byline__link::text").extract_first() ,
    content = response.css("p::text").extract(),
    image = response.css("figure.media--uneven div.media__item  picture img::attr(src)").extract(),
    time = response.css("span.story__time span.timestamp--time span.timestamp__time::text").extract(), 
    date = response.css("span.story__time span.timestamp--date::text").extract() 
    category = 'tech'
    source = 'DAWN'

    items['title'] = title
    items['author'] = author
    items['content'] = content
    items['image'] = image
    items['time'] = time
    items['date'] = date
    items['category'] = category
    items['source'] = source

    yield items

  def parseTribuneBusiness(self, response):
    items = WebscrapingItem()

    title = response.css('div.story-box-section h1::text').get()
    author = response.css('div.story-box-section span.storypage-leftside div.left-authorbox span a::text').get()
    content = response.css('div.story-box-section div.mainstorycontent-parent div.storypage-main-section2 div.storypage-rightside span.story-text p span::text').get().strip()
    image = response.css('div.story-box-section div.mainstorycontent-parent div.storypage-main-section2 div.storypage-rightside span.top-big-img div.story-featuredimage div.amp-top-main-img div.featured-image-global img::attr(src)').get()
    date = response.css('div.story-box-section span.storypage-leftside div.left-authorbox span::text')[1].get()
    time = response.xpath('//script[@type="application/ld+json"]/text()').get()
    category = 'business'
    source = 'Express Tribune'

    items['title'] = title
    items['author'] = author
    items['content'] = content
    items['image'] = image
    items['time'] = time
    items['date'] = date
    items['category'] = category
    items['source'] = source

    yield items

  def parseTribuneSports(self, response):
    items = WebscrapingItem()

    title = response.css('div.story-box-section h1::text').get()
    author = response.css('div.story-box-section span.storypage-leftside div.left-authorbox span a::text').get()
    content = response.css('div.story-box-section div.mainstorycontent-parent div.storypage-main-section2 div.storypage-rightside span.story-text p::text').get().strip()
    image = response.css('div.story-box-section div.mainstorycontent-parent div.storypage-main-section2 div.storypage-rightside span.top-big-img div.story-featuredimage div.amp-top-main-img div.featured-image-global img::attr(src)').get()
    date = response.css('div.story-box-section span.storypage-leftside div.left-authorbox span::text')[1].get()
    time = response.xpath('//script[@type="application/ld+json"]/text()').get()
    category = 'sports'
    source = 'Express Tribune'

    items['title'] = title
    items['author'] = author
    items['content'] = content
    items['image'] = image
    items['time'] = time
    items['date'] = date
    items['category'] = category
    items['source'] = source

    yield items  

  def parseTribuneTech(self, response):
    items = WebscrapingItem()

    title = response.css('div.story-box-section h1::text').get()
    author = response.css('div.story-box-section span.storypage-leftside div.left-authorbox span a::text').get()
    content = response.css('div.story-box-section div.mainstorycontent-parent div.storypage-main-section2 div.storypage-rightside span.story-text p::text').get().strip()
    image = response.css('div.story-box-section div.mainstorycontent-parent div.storypage-main-section2 div.storypage-rightside span.top-big-img div.story-featuredimage div.amp-top-main-img div.featured-image-global img::attr(src)').get()
    date = response.css('div.story-box-section span.storypage-leftside div.left-authorbox span::text')[1].get()
    time = response.xpath('//script[@type="application/ld+json"]/text()').get()
    category = 'sports'
    source = 'Express Tribune'

    items['title'] = title
    items['author'] = author
    items['content'] = content
    items['image'] = image
    items['time'] = time
    items['date'] = date
    items['category'] = category
    items['source'] = source

    yield items    