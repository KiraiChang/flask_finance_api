import requests
import sqlite3
import datetime
from lxml import etree
from flask_restful import Resource, reqparse

class Exchanges(Resource):
    insert_exchanges_query = 'INSERT INTO exchanges VALUES(?, ?, ?, ?, ?, ?, ?)'
    select_exchanges_max_date_query = 'SELECT date FROM exchanges ORDER BY date DESC LIMIT 1'
    select_exchanges_date_query = 'SELECT * FROM exchanges WHERE date >=? ORDER BY date DESC'

    def patch(self, date):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute(self.select_exchanges_max_date_query)
        endDate = datetime.datetime.now()
        maxDate = datetime.datetime.strptime(cursor.fetchone()[0], '%Y%m%d')
        exchangeParam = {
            "datestart":maxDate.strftime('%Y/%m/%d'),
            "syear":maxDate.strftime('%Y'),
            "smonth":maxDate.strftime('%m'),
            "sday":maxDate.strftime('%d'),
            "dateend":endDate.strftime('%Y/%m/%d'),
            "eyear":endDate.strftime('%Y'),
            "emonth":endDate.strftime('%m'),
            "eday":endDate.strftime('%d'),
        }
        #print(endDate, maxDate, exchangeParam)
        response = requests.post('http://www.taifex.com.tw/chinese/3/3_5.asp', exchangeParam)
        html = etree.HTML(response.content)
        exchangeList = []
        #print(html.xpath('//*[@id="printhere"]/div[3]/table/tbody/tr/td'))
        for item in html.xpath('//*[contains(@class, "table_c")]/tbody/tr'):
            # item[0].text->日期
            # item[1].text->美元／新台幣
            # item[3].text->美元／新台幣
            # item[5].text->英鎊／美元
            # item[6].text->澳幣／美元
            # item[10].text->紐幣／美元
            #print(item[0].text, item[1].text, item[3].text, item[5].text, item[6].text, item[10].text)
            if(item[0].text != None):
                itemDate = datetime.datetime.strptime(item[0].text, '%Y/%m/%d')
                if(maxDate < itemDate):
                    exchangeList.append((None, 
                                        itemDate.strftime('%Y%m%d'), 
                                        float(item[1].text),
                                        float(item[3].text),
                                        float(item[5].text),
                                        float(item[6].text),
                                        float(item[10].text)))

        if(len(exchangeList) > 0):
            cursor.executemany(self.insert_exchanges_query, exchangeList)
        conn.commit()
        conn.close()
        return {'message': 'patch fund success', 'funds': list(exchangeList)}, 200
    
    def get(self, date):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        exchangeList = []
        for row in cursor.execute(self.select_exchanges_date_query, (date,)):
            exchangeList.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        conn.commit()
        conn.close()
        return {'message': 'get fund success', 'funds': list(exchangeList)}, 200