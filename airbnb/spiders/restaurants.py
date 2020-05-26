# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from airbnb.items import *
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
import json




class RestaurantsSpider(scrapy.Spider):


	name = 'restaurants'


	def __init__(self, **kwargs):
		if not "city" in kwargs:
			raise CloseSpider('The city parameter is required!')
		else:
			super().__init__(**kwargs)


	def start_requests(self):
		yield scrapy.Request(url = f"https://www.airbnb.com.br/s/{city_process(self = self)}/things-to-do/food-restaurants/{category_process(self = self)}")


	def parse(self, response):
		html = Selector(text=response.body.decode("utf-8"))
		json_to_dict = json.loads(html.xpath('//script[@id="data-state"]/text()').get().replace(r'\\"','"'))
		places = json_to_dict.get("niobeClientData").get("__niobe_denormalized").get("queries")[0][1].get("dora").get("exploreV3").get("sections")[2].get("items")

		for place in places:
			yield scrapy.Request(	url = f"https://www.airbnb.com.br/things-to-do/places/{place['placeId']}",
									callback = self.final_parse,
									cb_kwargs = {
													"Id": place.get('placeId'),
													"Name": place.get('name'),
													"Category": place.get('primaryCategory'),
													"City": self.city[:self.city.index(",")],
													"State": self.city[-2:]
												}
								)
		
		relative_url = html.xpath('//li[@class="_i66xk8d"]/a/@href').get()

		if relative_url:
			absolute_url = response.urljoin(relative_url)

			yield scrapy.Request(url = absolute_url, callback = self.parse)


	def final_parse(self, response, Id, Name, Category, City, State):

		html = Selector(text=response.body.decode("utf8").replace(r"\'","'"))
		json_to_dict = json.loads(html.xpath('//script[@id="data-state"]/text()').get().replace(r'\\"','"'))
		place = json_to_dict.get('bootstrapData').get('reduxData').get("placePDP").get("placeData").get("product")
		
		loader = ItemLoader(item = AirbnbItem())

		loader.add_value("Id", Id)
		loader.add_value("Category", Category)
		loader.add_value("Name", Name)
		loader.add_value("City", City)
		loader.add_value("State", State)
		loader.add_value("Phone", place.get("phone"))
		loader.add_value("Address", place.get('address'))
		loader.add_value("ZipCode", place.get("zipcode"))
		loader.add_value("Rating", place.get('rating'))
		loader.add_value("image_urls", [item.get('original_picture') for item in place['cover_photos']])

		yield loader.load_item()

#--------------------
#parameter functions
#--------------------

def city_process(self):
	return f"{self.city[:self.city.index(',')].title().replace(' ', '-')}{'--'}{self.city[self.city.index(',') + 1::].strip().upper()}"


def category_process(self):
	
	place_category = ("restaurants", "cafes", "bakeries", "grocery-stores")

	if not 'category' in self.__dict__:
		return place_category[0]
	else:
		if self.category.lower() in place_category:
			return self.category.lower()
		else:
			return place_category[0]