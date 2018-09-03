# -*- coding: utf-8 -*-
import scrapy
import json
from jiudian.items import JiudianItem

class JdSpider(scrapy.Spider):
    name = 'jd'

    def start_requests(self):
        city_id = 1
        page = 0
        while page < 1000:
            start_api = "https://m.dianping.com/otahotel/hotelm/search?cityid={}&limitresult=20&limitpageno={}".format(city_id, page)
            page += 1
            yield scrapy.Request(start_api)

    def parse(self, response):
        res_json = json.loads(response.text)
        data_list = res_json["data"]["shopList"]
        for data in data_list:
            shop_id = data["shopId"]
            lowestPrice = data["lowestPrice"]
            #更过信息api，包含电话、设施那些
            detailInfo_api = "https://m.dianping.com/otahotel/hotelm/detailInfo?shopid={}".format(shop_id)
            yield scrapy.Request(detailInfo_api, callback=self.parse_detailInfo, meta={"shop_id":shop_id,"lowestPrice":lowestPrice})

    def parse_detailInfo(self, response):
        res_json = json.loads(response.text)
        shop_id = response.meta["shop_id"]
        data = res_json["data"]
        phone = data["shopInfos"]["phoneList"]
        #地址、装修等api
        hotelInfo_api = "https://m.dianping.com/hotelm/ajax/hotelInfo?shopId={}".format(shop_id)
        return scrapy.Request(hotelInfo_api, callback=self.parse_hotelInfo, meta={"phone":phone,"lowestPrice":response.meta["lowestPrice"]})

    def parse_hotelInfo(self, response):
        item = JiudianItem()
        res_json = json.loads(response.text)
        data = res_json["data"]
        #最低价
        lowestPrice = response.meta["lowestPrice"]
        #电话
        phone = response.meta["phone"]
        #酒店名称
        title = data["fullName"]
        #地址
        addr = data["address"]
        #区域
        quyu = data["crumbNavigate"][1]["name"]
        #城市
        city = data["crumbNavigate"][0]["name"]
        #店铺id
        shop_id = data["shopId"]

        item["title"] = title
        item["addr"] = addr
        item["lowestPrice"] = lowestPrice
        item["quyu"] = quyu
        item["phone"] = phone
        item["shop_id"] = shop_id
        item["city"] = city

        yield item