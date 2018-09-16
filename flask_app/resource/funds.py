import requests
import sqlite3
import datetime
from lxml import etree
from flask_restful import Resource
from models.fund import FundModel


class Funds(Resource):
    def patch(self, date):
        maxDate = datetime.datetime.strptime(FundModel.get_max_date(), '%Y%m%d')
        response = requests.get(
            "http://fund.bot.com.tw/w/wb/wb02a.djhtm?a=ALB04-0961")
        html = etree.HTML(response.content)
        fundList = []
        for item in html.xpath(
                '//*['
                'contains(@class, "wfb2c")'
                ' or contains(@class, "wfb5c")]/parent::tr'
        ):
            # every item have 4 column, less is not get correct item
            # item[0].text->date
            # item[1].text->price
            # item[2].text->up or down
            # item[3].text->up or down rate
            if (len(item) == 4):
                date = datetime.datetime.strptime(item[0].text, '%Y/%m/%d')
                if (maxDate < date):
                    fundList.append(FundModel(date.strftime('%Y%m%d'),
                                     item[1].text))
        if (len(fundList) > 0):
            FundModel.save_list_to_db(fundList)
        return {'message': 'patch fund success', 'funds': list(item.json() for item in fundList)}, 200

    def get(self, date):
        return {'message': 'get fund success', 'funds': list(item.json() for item in FundModel.get_by_date(date))}, 200
