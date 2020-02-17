# -*- coding: utf-8 -*-

##scrapy spider with a little preprocessing
import scrapy
from word2number import w2n


class BooksSpider(scrapy.Spider):
	name = 'books'
	allowed_domains = ['books.toscrape.com']
	start_urls = ['http://books.toscrape.com']

	def parse(self, response):

		for index,responses in enumerate(response.xpath('//article[@class="product_pod"]')):
			
			item= {
			"price":responses.xpath('.//p[@class="price_color"]/text()').extract()[0].replace("\u00a3",""),
			"name":responses.xpath('.//h3/a/@title').extract()[0],
			### w2n converts written Text Numbers into actual digits for database purposes
			"rating": w2n.word_to_num(responses.xpath('//p/@class').extract()[0].replace("star-rating","")),   
			"images" : "http://books.toscrape.com/"+responses.xpath('.//img/@src').extract()[0]}



			url = response.xpath('.//h3/a/@href').extract()[index]
			absoluteurl = response.urljoin(url)
			yield scrapy.Request(absoluteurl,meta={'item': item},dont_filter=True,callback=self.go_deeper)

		pagination = response.xpath('//li[@class="next"]/a/@href').extract_first()
		absolutepagination = response.urljoin(pagination)
		yield scrapy.Request(url = absolutepagination,callback=self.parse)


	def go_deeper(self, response):
		item = response.meta.get("item",{})

		item["upc"] = response.xpath('//tr/td').extract()[0].replace("<td>","").replace("</td>","")
		item["isavail"] = response.xpath('//p[@class="instock availability"]/text()').extract()[1].replace("\n","").replace("In stock (","").replace(")","").replace(" ","").replace("available","") 
		item["description"] = response.xpath('//p/text()').extract()[10]
		yield item                                                               
		
