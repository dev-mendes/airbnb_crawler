# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import *
from psycopg2 import connect



class PostgresPipeline():


	def __init__(self, pg_host, pg_port, pg_user, pg_pass, pg_dbname, pg_table):
		self.pg_host = pg_host
		self.pg_port = pg_port
		self.pg_user = pg_user
		self.pg_pass = pg_pass
		self.pg_dbname = pg_dbname
		self.pg_table = pg_table
		self.sql_table = f'''
								CREATE TABLE IF NOT EXISTS {pg_table} (
									id			integer NOT NULL,
									category	varchar(100) NOT NULL,
									name		varchar(50) NOT NULL,
									city		varchar(20),
									state		varchar(2),
									phone		varchar(15),
									address		varchar(50),
									zipcode		varchar(15),
									rating		varchar(15),
								PRIMARY KEY (id)
								);
							'''
		self.sql_insert = f'''
								INSERT INTO {pg_table} (id, category, name, city, state, phone, address, zipcode, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
							'''


	def open_spider(self, spider):
		self.conn = connect(host = self.pg_host, port = self.pg_port, dbname = self.pg_dbname, user = self.pg_user, password = self.pg_pass)
		self.cur = self.conn.cursor()
		self.cur.execute(self.sql_table)
		self.conn.commit()


	@classmethod
	def from_crawler(cls, crawler):
		return cls( pg_host = crawler.settings.get("PG_HOST"),
					pg_port = crawler.settings.get("PG_PORT", "5432"),
					pg_user = crawler.settings.get("PG_USER"),
					pg_pass = crawler.settings.get("PG_PASS"),
					pg_dbname = crawler.settings.get("PG_DBNAME"),
					pg_table = crawler.settings.get("PG_TABLE")
					)


	def process_item(self, item, spider):
		try:
			self.cur.execute(self.sql_insert, (
												item.get("Id")[0],
												item.get("Category")[0],
												item.get("Name")[0],
												item.get("City")[0],
												item.get("State")[0],
												item.get("Phone")[0] if item.get("Phone") else None,
												item.get("Address")[0] if item.get("Address") else None,
												item.get("ZipCode")[0] if item.get("ZipCode") else None,
												item.get("Rating")[0] if item.get("Rating") else None
												)
			)

			self.conn.commit()

		except Exception as e:
			self.conn.rollback()

		return item


	def close_spider(self, spider):
		self.cur.close()
		self.conn.close()


#-----------------------------------------------------------------------------------


class PhotoPipeline(ImagesPipeline):
    
    def open_spider(self, spider):
    	self.spiderinfo = self.SpiderInfo(spider)
    	self.city = spider.city

    def get_media_requests(self, item, info):
    	return [Request(x, meta={"place_id": item.get("Id")[0]}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
    	city_path = self.city
    	place_path = request.meta.get("place_id")
    	image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
    	return f'images/{city_path}/{place_path}/{image_guid}.jpg'