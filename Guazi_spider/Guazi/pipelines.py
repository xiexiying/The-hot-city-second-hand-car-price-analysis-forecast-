# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymongo
import csv


class GuaziPipeline(object):
    def process_item(self, item, spider):
        print(item['name'])
        return item

class GuaziCsv(object):
    def open_spider(self, spider):
        self.f=open('guazi.csv', 'a')
        self.writer = csv.writer(self.f)
    def process_item(self, item, spider):  # 数据处理
        li=[
            item['name'],item['s_price'],item['price'],item['time'],item['km'],item['displace'],item['typ'],
        ]

        self.writer.writerow(li)
        return item

    def close_spider(self, spider):
        self.f.close()
    #存到MySQL处理数据
# class GuaziMysqlPipeline(object):
#     def open_spider(self,spider):#爬虫开始时只执行一次，连接数据库
#         self.db=pymysql.connect('localhost','root','123456','cardb',charset='utf8')
#         self.cur=self.db.cursor()
#         self.ins='insert into cartab values(%s,%s,%s)'
#
#     def process_item(self, item, spider):#数据处理
#         li=[
#             item['name'],item['price'],item['href']
#         ]
#         self.cur.execute(self.ins,li)
#         self.db.commit()
#         return item
#
#     def close_spider(self, spider):
#         self.cur.close()
#         self.db.close()
        #存数据到mangodb
# class GuaziMongoPipeline(object):
#     def open_spider(self, spider):#连接数据库
#         self.conn=pymongo.MongoClient('localhost',27017)
#         self.db=self.conn['cardb']
#         self.myset=self.db['carset']
#     def process_item(self, item, spider):
#         self.myset.insert_one(dict(item))
#         return item

    # def close_spider(self, spider):
    #     sel