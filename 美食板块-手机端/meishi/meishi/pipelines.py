# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime

class MeishiPipeline(object):
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
            """replace into meishi_chengdu(updata_time, shop_name, address, phone, level, shop_id) value(%s, %s, %s, %s, %s, %s)""",
            (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                item["shop_name"],
                item["address"],
                item["phone"],
                item["level"],
                item["shop_id"]
                )
            )
        self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()

# CREATE TABLE meishi_chengdu (
#     auto_id INT NOT NULL primary key AUTO_INCREMENT,
#     updata_time DateTime NOT NULL,
#     shop_name VARCHAR(255),
#     address VARCHAR(255),
#     phone VARCHAR(100),
#     level VARCHAR(100),
#     shop_id VARCHAR(50));
# ALTER TABLE `meishi_chengdu` ADD UNIQUE (`shop_id`);