# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PythonQmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 名称
    name = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 多少人关注以及多久前发布的
    follow_release = scrapy.Field()
    # 小地址
    small_add = scrapy.Field()
    # 大地址
    big_add = scrapy.Field()
    # 房子情况
    houseInfo = scrapy.Field()
    # 总价格
    totalPrice = scrapy.Field()
    # 每平米价格
    Price_per_square_meter = scrapy.Field()

    #id
    ID = scrapy.Field()
    # 所属地区
    areaName = scrapy.Field()
    # 房屋朝向
    orientation = scrapy.Field()
    # 房屋类型
    type = scrapy.Field()
    # 所在楼层
    Floor = scrapy.Field()
    # 装修情况
    Decoration = scrapy.Field()
    # 套内面积
    Inside_area = scrapy.Field()
    # 是否配备电梯
    elevator = scrapy.Field()
    # 挂牌时间
    Listing_time = scrapy.Field()
    # 建筑年代
    building_age = scrapy.Field()
    # 小区的均价
    village_avg = scrapy.Field()
    # 交易权属
    T_ownership = scrapy.Field()

