# -*- coding: utf-8 -*-
# Define here the models for your scraped items
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import MapCompose, TakeFirst, Identity
import scrapy

#--------------------------
# input_processor functions
#--------------------------
def rating_process(data):
	if data:
		if len(str(data)) == 1:
			return str(data) + ".0"
		else:
			return str(data)[:3]
	else:
		return data

def zipcode_process(data):
	if data:
		return data.replace("-", "")
	else:
		return data

def phone_process(data):
	if data:
		for item in ["+", " ", "-", "(", ")"]:
			data = data.replace(item, "")
		return data
	else:
		return data



class AirbnbItem(scrapy.Item):
	Id = scrapy.Field()
	Category = scrapy.Field()
	Name = scrapy.Field()
	City = scrapy.Field()
	State = scrapy.Field()
	Phone = scrapy.Field( input_processor = MapCompose(phone_process) )
	Address = scrapy.Field()
	ZipCode = scrapy.Field( input_processor = MapCompose(zipcode_process) )
	Rating = scrapy.Field( input_processor = MapCompose(rating_process) )
	image_urls = scrapy.Field()
	images = scrapy.Field()


