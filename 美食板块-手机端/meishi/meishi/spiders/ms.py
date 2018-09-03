# -*- coding: utf-8 -*-
import scrapy
import re
from meishi.items import MeishiItem


class MsSpider(scrapy.Spider):
    name = 'ms'

    def start_requests(self):
        for page in range(0,5001,50):
            url = "https://mapi.dianping.com/searchshop.json?start={}&categoryid=10&parentCategoryId=10&locatecityid=0&limit=50&sortid=0&cityid=8&range=-1&maptype=0".format(str(page))
            yield scrapy.Request(url)

    def parse(self, response):
        shop_ids = re.findall(r'"id":"(\d+)"',response.text)
        for shop_id in shop_ids:
            url = "https://m.dianping.com/shop/" + shop_id
            yield scrapy.Request(url, callback=self.parse_shop)

    def parse_shop(self, response):
        item = MeishiItem()
        shop_id = response.url.split("shop/")[1]

        shop_name = re.findall(r'<h1 class="shop-name">(.*?)</h1>',response.text)[0]

        address = re.findall(r'<i class="icon-address"></i>([\S\s]+?)<i',response.text)[0].replace("\n","")

        phone = re.findall(r'href="tel:(.*?)"',response.text)
        phone = phone[0] if len(phone)==1 else str(phone)

        level = re.findall(r'<span class="star star-(\d+)"></span>',response.text)[0]
        level = str(int(level)/10)


        item["shop_id"] = shop_id
        item["shop_name"] = shop_name
        item["address"] = address
        item["phone"] = phone
        item["level"] = level

        yield item