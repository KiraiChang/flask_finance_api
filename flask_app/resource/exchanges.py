import requests
import sqlite3
import datetime
from lxml import etree
from flask_restful import Resource
from models.exchange import ExchangeModel


class ExchangesResource(Resource):
    def patch(self, date):
        endDate = datetime.datetime.now()
        maxDate = datetime.datetime.strptime(
            ExchangeModel.get_max_date(), '%Y%m%d')
        exchangeParam = {
            "queryStartDate": maxDate.strftime('%Y/%m/%d'),
            "queryEndDate": endDate.strftime('%Y/%m/%d'),
        }
        # print(exchangeParam)

        response = requests.post('http://www.taifex.com.tw/cht/3/dailyFXRate',
                                 exchangeParam)
        html = etree.HTML(response.content)
        exchangeList = []

        for item in html.xpath('//*[contains(@class, "table_c")]/tbody/tr'):
            # item[0].text->日期
            # item[1].text->美元／新台幣
            # item[3].text->美元／新台幣
            # item[5].text->英鎊／美元
            # item[6].text->澳幣／美元
            # item[10].text->紐幣／美元s

            if item[0].text is not None:
                itemDate = datetime.datetime.strptime(item[0].text, '%Y/%m/%d')
                if (maxDate < itemDate):
                    exchangeList.append(ExchangeModel(itemDate.strftime('%Y%m%d'),
                                                      float(item[1].text),
                                                      float(item[3].text),
                                                      float(item[5].text),
                                                      float(item[6].text),
                                                      float(item[10].text)))

        if (len(exchangeList) > 0):
            ExchangeModel.save_list_to_db(exchangeList)
        return {
            'message': 'patch exchange success',
            'exchange': list(item.json() for item in exchangeList)
        }, 200

    def get(self, date):
        return {
            'message': 'get exchange success',
            'exchange': list(item.json() for item in ExchangeModel.get_by_date(date))
        }, 200
