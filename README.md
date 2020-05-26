# airbnb_crawler
Airbnb Restaurants Crawler

Features
--------

* PostgreSQL

    Store scraped data directly in your PostgreSql database.

* ImagesPipeline

    Download all images of the restaurants.

* User-Agent Rotator Middleware
  
    Prevents your ip from being blocked by sending random "User-Agent".
    
Requirements
------------
* Python 3
* Scrapy 2.0.1
* psycopg2_binary 2.8.5
* psycopg2 2.8.5

Usage
-----


Restaurants are searched by city and state

Run the crawler
    >>> cd airbnb-project
    >>> scrapy crawl restaurants -a city="Denver, CO"
    >>> scrapy crawl restaurants -a city="New York, NY"

The crawler accepts the additional parameter "category", which can be: "cafes", "bakeries", "grocery-stores", "restaurants"

    >>> cd airbnb-project
    >>> scrapy crawl restaurants -a city="Denver, CO" -a category="cafes"
    >>> scrapy crawl restaurants -a city="New York, NY" -a category="bakeries"
