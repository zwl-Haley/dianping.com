# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime

class JiudianPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = "127.0.0.1",
            port = 3306,
            db = "dianping",
            user = "root",
            passwd = "",
            charset = "utf8",
            use_unicode = True
            )
        self.cursor = self.connect.cursor()
        print("链接MySQL数据库成功！")

    def process_item(self, item, spider):
        self.cursor.execute(
            """replace into jiudian(updata_time, city, shopId, title, quyu, addr, lowestPrice, phone) value(%s, %s, %s, %s, %s, %s, %s, %s)""",
            (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                item["city"],
                item["shop_id"],
                item["title"],
                item["quyu"],
                item["addr"],
                item["lowestPrice"],
                str(item["phone"])
                )
            )
        self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()

# CREATE TABLE jiudian (
#     auto_id INT NOT NULL primary key AUTO_INCREMENT,
#     updata_time DateTime NOT NULL,
#     city VARCHAR(20),
#     shopId VARCHAR(20),
#     title VARCHAR(50),
#     quyu VARCHAR(20),
#     addr VARCHAR(100),
#     lowestPrice VARCHAR(10),
#     phone VARCHAR(50));
# ALTER TABLE `jiudian` ADD UNIQUE (`poiid`);