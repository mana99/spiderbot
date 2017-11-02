# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#class FantacalcioPipeline(object):
#    def process_item(self, item, spider):
#        return item

#import sys
#import MySQLdb
#import hashlib
#from scrapy.exceptions import DropItem
#from scrapy.http import Request


# See https://github.com/rolando/dirbot-mysql/
from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi


class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        guid = self._get_guid(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM fantatable WHERE guid = %s
        )""", (guid, ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE fantatable
                SET nome=%s, numero=%s, ruolo=%s, squadra=%s, stagione=%s, giornata=%s,
                    voto=%s, gol=%s, assist=%s, rigore=%s, rigore_sbagliato=%s,
                    autogol=%s, ammonizione=%s, espulsione=%s, fantavoto=%s, updated=%s
                WHERE guid=%s
            """, (item['nome'][0], \
                    item['numero'][0], \
                    item['ruolo'][0], \
                    item['squadra'][0], \
                    item['stagione'][0], \
                    item['giornata'][0], \
                    item['voto'][0], \
                    item['gol'][0], \
                    item['assist'][0], \
                    item['rigore'][0], \
                    item['rigore_sbagliato'][0], \
                    item['autogol'][0], \
                    item['ammonizione'][0], \
                    item['espulsione'][0], \
                    item['fantavoto'][0], \
                    now, \
                    guid))
            spider.log("Item updated in db: %s %r" % (guid, item))
        else:
            conn.execute("""
                INSERT INTO fantatable (
                    guid, nome, numero, ruolo, squadra, stagione, giornata,
                    voto, gol, assist, rigore, rigore_sbagliato,
                    autogol, ammonizione, espulsione, fantavoto, updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (guid, \
                    item['nome'][0], \
                    item['numero'][0], \
                    item['ruolo'][0], \
                    item['squadra'][0], \
                    item['stagione'][0], \
                    item['giornata'][0], \
                    item['voto'][0], \
                    item['gol'][0], \
                    item['assist'][0], \
                    item['rigore'][0], \
                    item['rigore_sbagliato'][0], \
                    item['autogol'][0], \
                    item['ammonizione'][0], \
                    item['espulsione'][0], \
                    item['fantavoto'][0], \
                    now))
            spider.log("Item stored in db: %s %r" % (guid, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item['nome'][0].encode('utf-8')+item['giornata'][0].encode('utf-8')+item['stagione'][0].encode('utf-8')).hexdigest()

