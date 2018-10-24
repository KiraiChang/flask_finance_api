import requests
import sqlite3
import datetime
from lxml import etree
from flask_restful import Resource
from models.stock import StockModel


class StocksResource(Resource):
    def patch(self, date):
        maxDate = datetime.datetime.strptime(
            StockModel.get_max_date(), '%Y%m%d')
        response = requests.get(
            'http://www.twse.com.tw/exchangeReport'
            '/STOCK_DAY?response=html&date='
            + date + "&stockNo=0050")
        html = etree.HTML(response.content)
        stockList = []
        for item in html.xpath('/html/body/div/table/tbody/tr'):
            # item[0].text->日期
            # item[3].text->開盤價
            # item[4].text->最高價
            # item[5].text->最低價
            # item[6].text->收盤價
            # item[7].text->漲跌價差
            # item[1].text->成交股數
            # item[2].text->成交金額
            # 日期民國轉西元
            year = int(item[0].text.split('/')[0]) + 1911
            month = int(item[0].text.split('/')[1])
            day = int(item[0].text.split('/')[2])
            itemDate = datetime.datetime(year, month, day)
            if (maxDate < itemDate):
                stockList.append(
                    StockModel(itemDate.strftime('%Y%m%d'), float(item[3].text),
                               float(item[4].text), float(item[5].text),
                               float(item[6].text), float(item[7].text),
                               round(
                                   int(item[1].text.replace(',', '')) / 1000),
                               round(int(item[2].text.replace(',', '')) / 1000)))
        if (len(stockList) > 0):
            StockModel.save_list_to_db(stockList)
        return {'message': 'patch fund success', 'funds': list(item.json() for item in stockList)}, 200

    def get(self, date):
        return {'message': 'get fund success', 'funds': list(item.json() for item in StockModel.get_by_date(date))}, 200
