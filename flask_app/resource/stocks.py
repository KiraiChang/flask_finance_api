import requests
import sqlite3
import datetime
from lxml import etree
from flask_restful import Resource, reqparse

class Stocks(Resource):
    insert_stock_query = 'INSERT INTO stocks VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'
    select_stock_max_date_query = 'SELECT date FROM stocks ORDER BY date DESC LIMIT 1'
    select_stock_date_query = 'SELECT * FROM stocks WHERE date >=? ORDER BY date DESC'

    def patch(self, date):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute(self.select_stock_max_date_query)
        maxDate = datetime.datetime.strptime(cursor.fetchone()[0], '%Y%m%d')
        response = requests.get("http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date="+date+"&stockNo=0050")
        html = etree.HTML(response.content)
        stockList = []
        for item in html.xpath('/html/body/div/table/tbody/tr'):
            #item[0].text->日期
            #item[3].text->開盤價
            #item[4].text->最高價
            #item[5].text->最低價
            #item[6].text->收盤價
            #item[7].text->漲跌價差
            #item[1].text->成交股數
            #item[2].text->成交金額
            #日期民國轉西元
            year = int(item[0].text.split('/')[0]) + 1911
            month = int(item[0].text.split('/')[1])
            day = int(item[0].text.split('/')[2])
            itemDate = datetime.datetime(year, month, day)
            if(maxDate < itemDate):
                stockList.append((None, 
                                    itemDate.strftime('%Y%m%d'), 
                                    float(item[3].text),
                                    float(item[4].text),
                                    float(item[5].text),
                                    float(item[6].text),
                                    float(item[7].text),
                                    round(int(item[1].text.replace(',', '')) / 1000),
                                    round(int(item[2].text.replace(',', '')) / 1000)))
        if(len(stockList) > 0):
            cursor.executemany(self.insert_stock_query, stockList)
        conn.commit()
        conn.close()
        return {'message': 'patch fund success', 'funds': list(stockList)}, 200
    
    def get(self, date):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        stockList = []
        for row in cursor.execute(self.select_stock_date_query, (date,)):
            stockList.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        conn.commit()
        conn.close()
        return {'message': 'get fund success', 'funds': list(stockList)}, 200