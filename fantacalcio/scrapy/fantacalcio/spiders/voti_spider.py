import scrapy
from fantacalcio.items import PlayerItem


class VotiSpider(scrapy.Spider):
    name = "voti"
    allowed_domains = ["gazzetta.it"]
    start_urls = ["http://www.gazzetta.it/calcio/fantanews/voti/serie-a-2017-18/",
                  "http://www.gazzetta.it/calcio/fantanews/voti/serie-a-2016-17/",
                  "http://www.gazzetta.it/calcio/fantanews/voti/serie-a-2015-16/",
                  "http://www.gazzetta.it/calcio/fantanews/voti/serie-a-2014-15/",
                  "http://www.gazzetta.it/calcio/fantanews/voti/serie-a-2013-14/"]

    def parse(self, response):
        stagione = response.url[-8:-1]
        for href in response.css("ul.menuDaily > li > a::attr('href')"):
            full_url = response.urljoin(href.extract())
            # yield scrapy.Request(full_url, callback=self.parseMatchDay)
            # see http://bit.ly/2swSKT8
            request = scrapy.Request(full_url, callback=self.parseMatchDay)
            request.meta['stagione'] = stagione
            yield request

    def parseMatchDay(self, response):
        # print(type(response))  # class 'scrapy.http.response.html.HtmlResponse'
        matchDay = response.xpath('//div[@class="magicDayList listView magicDayListChkDay"]/h4/text()').extract()
        for sel in response.xpath('//div[@class="magicDayList listView magicDayListChkDay"]/div/div'):
            # print(type(sel)) # class 'scrapy.selector.unified.SelectorList'
            # print(type(sel.extract())) # type 'unicode'
            for team in sel.xpath('ul[@class="magicTeamList"]'):
                teamName=team.xpath('li/div[@class="teamName"]/span[@class="teamNameIn"]/text()').extract()
                for player in team.xpath('li'):
                    item = PlayerItem()
                    item['nome'] = player.xpath('div[@class="playerName"]/div/span[@class="playerNameIn"]/a/text()').extract()
                    item['numero'] = player.xpath('div[@class="playerName"]/div/span[@class="playerNumber"]/text()').extract()
                    item['ruolo'] = player.xpath('div[@class="playerName"]/div/span[@class="playerRole"]/text()').extract()
                    item['squadra'] = teamName
                    item['stagione'] = [ response.meta['stagione'] ]
                    item['giornata'] = matchDay
                    item['voto'] = player.xpath('div[2]/text()').extract()
                    item['gol'] = player.xpath('div[3]/text()').extract()
                    item['assist'] = player.xpath('div[4]/text()').extract()
                    item['rigore'] = player.xpath('div[5]/text()').extract()
                    item['rigore_sbagliato'] = player.xpath('div[6]/text()').extract()
                    item['autogol'] = player.xpath('div[7]/text()').extract()
                    item['ammonizione'] = player.xpath('div[8]/text()').extract()
                    item['espulsione'] = player.xpath('div[9]/text()').extract()
                    item['fantavoto'] = player.xpath('div[10]/text()').extract()
                    yield item
