# -*- coding: utf-8 -*-
import scrapy
import csv

with open("AllData.csv","a") as f:
    writer = csv.writer(f)
    writer.writerow(['URL','Title','Price','Category','Store','Location','Sells'])

class MercaSpider(scrapy.Spider):
    name = 'merca'
    allowed_domains = ['mercadolibre.com']
    start_urls = ['https://www.mercadolibre.com.ar/categories.html']

    def parse(self, response):
        links = response.xpath('.//*[@class="ch-g1-3"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(link,callback=self.getcategorydata,dont_filter=True)

    def getcategorydata(self,response):
        links = response.xpath('.//*[@class="item__info-link item__js-link "]/@href').extract()
        for link in links:
            yield scrapy.Request(link,callback=self.getdata,dont_filter=True)

        nextlink = response.xpath('.//*[@class="pagination__next"]/a/@href').extract_first()
        if nextlink:
            yield scrapy.Request(nextlink,callback=self.getcategorydata,dont_filter=True)


    def getdata(self,response):
        title = response.xpath('.//*[@class="item-title__primary "]/text()').extract_first().strip()
        price = response.xpath('.//*[@class="price-tag-fraction"]/text()').extract_first()
        category = ' > '.join([i.strip() for i in response.xpath('.//*[@class="vip-navigation-breadcrumb-list"]/li/a/text()').extract()])
        sells = ' '.join(response.xpath('.//*[@class="reputation-info block"]/dl/dd[1]//text()').extract()).strip()

        link = response.xpath('.//*[@class="reputation-view-more card-block-link"]/@href').extract_first()
        if link:
            yield scrapy.Request(link,callback=self.getalldata,meta={
                'title':title,
                'price':price,
                'category':category,
                'sells':sells,
                'url':response.url
            },dont_filter=True)

    def getalldata(self,response):
        store = response.xpath('.//*[@id="store-info__name"]/text()').extract_first()
        location = response.xpath('.//*[@class="location__description"]/text()').extract_first()

        with open("AllData.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([response.meta.get('url'),response.meta.get('title'),response.meta.get('price'),response.meta.get('category'),store,location,response.meta.get('sells')])
            print([response.meta.get('title'),response.meta.get('price'),response.meta.get('category'),store,location,response.meta.get('sells')])