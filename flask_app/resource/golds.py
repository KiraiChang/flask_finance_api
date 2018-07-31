import requests
import sqlite3
import datetime
from lxml import etree
from flask_restful import Resource, reqparse

class Golds(Resource):
    insert_gold_query = 'INSERT INTO golds VALUES(?, ?, ?, ?)'
    select_gold_max_date_query = 'SELECT date FROM golds ORDER BY date DESC LIMIT 1'
    select_gold_date_query = 'SELECT * FROM golds WHERE date >=? ORDER BY date DESC'

    def patch(self, date):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute(self.select_gold_max_date_query)
        maxDate = datetime.datetime.strptime(cursor.fetchone()[0], '%Y%m%d')
        response = requests.get("https://rate.bot.com.tw/gold/chart/ltm/TWD")
        html = etree.HTML(response.content)
        goldList = []
        for item in html.xpath('/html/body/div[contains(@class, "page-wrapper")]/main/div[contains(@class, "container")]/table/tbody/tr'):
            # item[0][0].text->date
            # item[1].text->currency
            # item[2].text->unit
            # item[3].text->buy
            # item[4].text->sell
            itemDate = datetime.datetime.strptime(item[0][0].text, '%Y/%m/%d')
            if(maxDate < itemDate):
                goldList.append((None, itemDate.strftime('%Y%m%d'), item[3].text, item[4].text))
        if(len(goldList) > 0):
            cursor.executemany(self.insert_gold_query, goldList)
        conn.commit()
        conn.close()
        return {'message': 'patch gold success', 'golds': list(goldList)}, 200

    def get(self, date):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        goldList = []
        for row in cursor.execute(self.select_gold_date_query, (date,)):
            goldList.append((row[0], row[1], row[2], row[3]))
        conn.commit()
        conn.close()
        return {'message': 'get gold success', 'golds': list(goldList)}, 200