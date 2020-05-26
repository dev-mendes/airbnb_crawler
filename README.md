# airbnb_crawler
Features
--------

* Distributed crawling/scraping

    You can start multiple spider instances that share a single redis queue.
    Best suitable for broad multi-domain crawls.

* Distributed post-processing

    Scraped items gets pushed into a redis queued meaning that you can start as
    many as needed post-processing processes sharing the items queue.

* Scrapy plug-and-play components
  
    Scheduler + Duplication Filter, Item Pipeline, Base Spiders.
