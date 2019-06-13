import requests
import sqlite3
import datetime
from lxml import etree
from flask_restful import Resource
from models.gold import GoldModel


class GoldsResource(Resource):
    def patch(self, date):
        maxDate = datetime.datetime.strptime(
            GoldModel.get_max_date(), '%Y%m%d')
        response = requests.get("https://rate.bot.com.tw/gold/chart/year/TWD")
        html = etree.HTML(response.content)
        goldList = []
        for item in html.xpath(
                '/html/body/div[contains(@class, "page-wrapper")]'
                '/main/div[contains(@class, "container")]/table/tbody/tr'):
            # item[0][0].text->date
            # item[1].text->currency
            # item[2].text->unit
            # item[3].text->buy
            # item[4].text->sell
            itemDate = datetime.datetime.strptime(item[0][0].text, '%Y/%m/%d')
            if (maxDate < itemDate):
                goldList.append(GoldModel(itemDate.strftime('%Y%m%d'),
                                          item[3].text, item[4].text))
        if (len(goldList) > 0):
            goldList = sorted(goldList, key=lambda g: g.date)
            GoldModel.save_list_to_db(goldList)
        return {'message': 'patch gold success', 'golds': list(item.json() for item in goldList)}, 200

    def get(self, date):
        return {'message': 'get gold success', 'golds': list(item.json() for item in GoldModel.get_by_date(date))}, 200
