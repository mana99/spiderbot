# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    name = scrapy.Field()
    city = scrapy.Field()
    website = scrapy.Field()
    size = scrapy.Field()
    company_type = scrapy.Field()
    revenue = scrapy.Field()
    headquarters = scrapy.Field()
    founded = scrapy.Field()
    industry = scrapy.Field()
    competitors = scrapy.Field()
    rating = scrapy.Field()
    recommend = scrapy.Field()
    ceo_approve = scrapy.Field()
    description = scrapy.Field()

