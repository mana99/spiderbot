import scrapy
from glassdoor.items import CompanyItem


class companySpider(scrapy.Spider):

    name = "company"
    allowed_domains = ["glassdoor.com"]

    def __init__(self, city='', url='', *args, **kwargs):
        super(companySpider, self).__init__(*args, **kwargs)

        #self.start_urls = ["https://www.glassdoor.com/Reviews/%s-reviews-SRCH_IL.0,9_IM1112.htm" % city.replace(' ', '-')]
        self.start_urls = [ url ]
        self.city = city


    def parse(self, response):
        city=self.city
        for company in response.xpath('//*[@id="MainCol"]/div[1]/div'):
            href = company.xpath('//div[1]/div[2]/div[1]/a/@href')
            for h in href.extract():
                print('https://www.glassdoor.com'+h)
                full_url = 'https://www.glassdoor.com'+h
                # yield scrapy.Request(full_url, callback=self.parseMatchDay)
                # see http://bit.ly/2swSKT8
                request = scrapy.Request(full_url, callback=self.parseCompany)
                yield request
        next_page = response.xpath('//*[@id="FooterPageNav"]/div/ul/li[7]/a/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parseCompany(self, response):
        item = CompanyItem()
        item['name'] = response.xpath('//*[@id="EmpHeroAndEmpInfo"]/div[3]/div[2]/h1/text()').extract_first()
        item['city'] = self.city
        item['website'] = response.xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[label="Website"]/span/a/text()').extract_first()
        item['size'] = response.xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[label="Size"]/span/text()').extract_first()
        item['company_type'] = response.xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[label="Type"]/span/text()').extract_first()
        item['revenue'] = response.xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[label="Revenue"]/span/text()').extract_first()
        item['headquarters'] = response.xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[label="Headquarters"]/span/text()').extract_first()
        item['founded'] = response.xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[label="Founded"]/span/text()').extract_first()
        item['industry'] = response.xpath('   //*[@id="EmpBasicInfo"]/div[1]/div/div[label="Industry"]/span/text()').extract_first()
        item['competitors'] = response.xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[label="Competitors"]/span/text()').extract_first()
        item['rating'] = response.xpath('//*[@id="EmpStats"]/div/div[1]/div[1]/text()').extract_first()
        #item['recommend'] = response.xpath('  //*[@id="EmpStats_Recommend"]/svg/text/text()').extract_first()
        item['recommend'] = response.xpath('//*[@id="EmpStats_Recommend"]/@data-percentage').extract_first()
        #item['ceo_approve'] = response.xpath('//*[@id="EmpStats_Approve"]/svg/text/text()').extract_first()
        item['ceo_approve'] = response.xpath('//*[@id="EmpStats_Approve"]/@data-percentage').extract_first()
        item['description'] = response.xpath('//*[@id="EmpBasicInfo"]/div[2]/div[1]/text()').extract_first()
        yield item
