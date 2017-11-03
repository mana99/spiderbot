# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# See https://github.com/rolando/dirbot-mysql/
from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi


class CleanFieldsPipeline(object):
    """A pipeline to ensure the item have the required fields."""

    required_fields = ('name',
                        'website',
                        'size',
                        'company_type',
                        'revenue',
                        'headquarters',
                        'founded',
                        'industry',
                        'competitors',
                        'rating',
                        'recommend',
                        'ceo_approve')

    def process_item(self, item, spider):
        for field in self.required_fields:
            if item.get(field):
                item[field]=item.get(field).strip()
        return item


class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    words_to_filter = ['politics', 'religion']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            desc = item.get('description') or ''
            if word in desc.lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item

class RequiredFieldsPipeline(object):
    """A pipeline to ensure the item have the required fields."""

    required_fields = ('name', 'description', 'url')

    def process_item(self, item, spider):
        for field in self.required_fields:
            if not item.get(field):
                raise DropItem("Field '%s' missing: %r" % (field, item))
        return item
