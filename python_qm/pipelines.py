# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
import csv
import pymysql
from openpyxl.compat import file

def dbHandle():

    conn = pymysql.connect(host='localhost',user='root',password='123456',db='house_2')
    return conn


class PythonQmPipeline(object):
    def process_item(self, item, spider):
        print(item)
        dbobject = dbHandle()
        cursor = dbobject.cursor()
        cursor.execute("USE house_2")
        # 插入数据库
        sql = 'insert into house_2.ef(name,link,follow_release,small_add,big_add,houseInfo,totalPrice,Price_per_square_meter,areaName,ID,orientation,type,Floor,Decoration,Inside_area,elevator,Listing_time,T_ownership) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql, (
                item['name'], item['link'], item['follow_release'], item['small_add'], item['big_add'], item['houseInfo'],
                item['totalPrice'], item['Price_per_square_meter'],
                item['areaName'], item['ID'], item['orientation'], item['type'], item['Floor'], item['Decoration'],
                item['Inside_area'], item['elevator'], item['Listing_time'], item['T_ownership']))
            cursor.connection.commit()
        except BaseException as e:
            print("错误出现:", e)
            dbobject.rollback()
        print(item)
        return item
    # wb = Workbook()
    # ws = wb.active
    # # 设置表头
    # ws.append(['名称','详情页链接','多少人关注以及多久前发布的','地址','房屋信息','价格','每平米价格',
    #            '所属地区','房屋类型','套内面积','挂牌时间','上一次交易时间','核心卖点','小区介绍',
    #            '交通出行','户型介绍'])
    # def process_item(self, item, spider):
    #     line = [item['name'],item['link'],item['follow_release'],item['address'],item['houseInfo'],item['totalPrice'],item['Price_per_square_meter'],
    #             item['areaName'],item['type'],item['Inside_area'],item['Listing_time'],item['Last_transaction_time'],item['Core_selling_points'],item['Introduction_to_community'],
    #             item['Transportation'],item['house_type']]
    #     self.ws.append(line) #按行添加
    #     self.wb.save('重庆九区二手房数据.xlsx')
    #     return item
    #     f = file('重庆九区二手房数据.csv','a+')
    #     writer = csv.writer(f)
    #     writer.writerow((item['name'],item['link'],item['follow_release'],item['address'],item['houseInfo'],item['totalPrice'],item['Price_per_square_meter'],
    #             item['areaName'],item['type'],item['Inside_area'],item['Listing_time'],item['Last_transaction_time'],item['Core_selling_points'],item['Introduction_to_community'],
    #             item['Transportation'],item['house_type']))
    #     return item