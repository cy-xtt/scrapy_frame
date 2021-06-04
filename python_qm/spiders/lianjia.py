# -*- coding: utf-8 -*-
import scrapy
import re
from lxml import etree
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import time
import random
from ..items import PythonQmItem

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    #主城9区 渝中区、大渡口区、江北区、沙坪坝区、九龙坡区、南岸区、北碚区、渝北区、巴南区
    start_urls = []
    list_x = ['yuzhong','dadukou','jiangbei','shapingba','jiulongpo','nanan','beibei','yubei','banan']
    for j in list_x:
        for i in range(1, 80):
            url1 = 'https://cq.lianjia.com/ershoufang/{}/pg{}/'.format(j,i)
            start_urls.append(url1)
    rules = (Rule(LinkExtractor(allow=r'book/\d+'), callback="parse"))
    def parse(self, response):
        div_list = response.xpath('//ul[@class="sellListContent"]/li')
        for i in div_list:
            item = PythonQmItem()
            # 详情页链接
            item['link'] = i.xpath('./div[@class="info clear"]/div[@class="title"]/a/@href').extract_first()
            # 名称
            item['name'] = i.xpath('./div[@class="info clear"]/div[@class="title"]/a/text()').extract_first()
            # 多少人关注以及多久前发布的
            item['follow_release'] = i.xpath('./div[@class="info clear"]/div[@class="followInfo"]/text()').extract_first()
            # 地址
            item['small_add'] = i.xpath('./div[@class="info clear"]/div[@class="flood"]/div/a[1]/text()').extract_first()
            # 地区
            item['big_add'] = i.xpath('./div[@class="info clear"]/div[@class="flood"]/div/a[2]/text()').extract_first()
            # 房屋信息
            item['houseInfo'] = i.xpath('./div[@class="info clear"]/div[@class="address"]/div/text()').extract_first()
            # 价格
            item['totalPrice'] = i.xpath(
                './div[@class="info clear"]/div[@class="priceInfo"]/div[1]/span/text()').extract_first()
            # 每平米价格
            item['Price_per_square_meter'] = i.xpath(
                './div[@class="info clear"]/div[@class="priceInfo"]/div[2]/span/text()').extract_first()
            # print(item['name'])

            yield scrapy.Request(item['link'], callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        #房屋id
        item['ID'] = response.xpath('/html/body/div[5]/div[2]/div[5]/div[4]/span[2]/text()').extract()
        #所属地区
        item['areaName'] = response.xpath('//div[@class="aroundInfo"]/div[@class="areaName"]/span[@class="info"]/a[1]/text()').extract()
        #房屋朝向
        item['orientation'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[7]/text()').extract()
        #房屋类型
        item['type'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[1]/text()').extract()
        #所在楼层
        item['Floor'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[2]/text()').extract()
        #装修情况
        item['Decoration'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[9]/text()').extract()
        #套内面积
        item['Inside_area'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[5]/text()').extract()
        #是否配备电梯
        item['elevator'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[11]/text()').extract()
        # 挂牌时间
        item['Listing_time'] = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[1]/span[2]/text()').extract()
        # 建筑年代
        item['building_age'] = response.xpath('//div[@class="xiaoqu_main fl"]/div[2]/span[@class="xiaoqu_main_info"]/text()').extract()
        #小区的均价
        village_avg = response.xpath('//*[@id="resblockCardContainer"]/div/div/div[2]/div/div[1]/span/text()').extract()
        item['village_avg'] = re.sub("\s","", ",".join(village_avg))
        #交易权属  商品房、别墅等等
        item['T_ownership'] = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[2]/span[2]/text()').extract()


        time.sleep(random.randint(1, 3))
        yield item

