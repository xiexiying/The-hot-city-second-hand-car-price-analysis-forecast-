# -*- coding: utf-8 -*-
import scrapy
from ..items import GuaziItem


class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['www.guazi.com']
    # start_urls = ['https://www.guazi.com/bj/buy']
    url = 'https://www.guazi.com/bj/buy/o{}/#bread'

    def start_requests(self):
        for o in range(1, 51):
            p_url = self.url.format(o)
            yield scrapy.Request(url=p_url, callback=self.parse)  # 交给调度器入队列

    def parse(self, response):  # 一级页面解析
        x = '//ul[@class="carlist clearfix js-top"]/li'
        li_list = response.xpath(x)
        for li in li_list:
            item = GuaziItem()
            item['href'] = 'https://www.guazi.com' + li.xpath('./a/@href').get()  # 将二级链接交给调度器入队列
            item['name'] = li.xpath('./a/@title').get()
            item['s_price'] = li.xpath('.//div[@class="t-price"]/em/text()').get()
            item['price'] = li.xpath('.//div[@class="t-price"]/p/text()').get()
            item['time']=li.xpath('.//div[@class="t-i"]/text()').get()
            yield scrapy.Request(url=item['href'],  # 将二级链接交给调度器入队列
                                 meta={'item': item},  # 在不同的函数中传递数据
                                 callback=self.detail_page)
            # yield item  # 交给管道处理数据

    def detail_page(self, response):  # 二级页面解析--提取汽车的行驶里程、排量
        # 接收meta作为response的一个属性传递过来
        item = response.meta['item']
        item['km'] = response.xpath('//ul[@class="assort clearfix"]/li[2]/span/text()').get()
        item['displace'] = response.xpath('//ul[@class="assort clearfix"]/li[3]/span/text()').get()
        item['typ'] = response.xpath('//ul[@class="assort clearfix"]/li[4]/span/text()').get()
        # item['s_price'] = response.xpath('//div[@class="price-origin no-jr"]/text()').get()
        yield item  # 交给管道处理数据