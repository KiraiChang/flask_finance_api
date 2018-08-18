import requests
import sqlite3
import datetime
from lxml import etree
from flask_restful import Resource


class Funds(Resource):
    insert_fund_query = 'INSERT INTO funds VALUES(?, ?, ?)'
    select_fund_max_date_query = ('SELECT date FROM funds'
                                  ' ORDER BY date DESC LIMIT 1')
    select_fund_date_query = ('SELECT * FROM funds'
                              ' WHERE date >=? ORDER BY date DESC')

    def patch(self, date):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute(self.select_fund_max_date_query)
        maxDate = datetime.datetime.strptime(cursor.fetchone()[0], '%Y%m%d')
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
                    fundList.append((None, date.strftime('%Y%m%d'),
                                     item[1].text))
        if (len(fundList) > 0):
            cursor.executemany(self.insert_fund_query, fundList)
        conn.commit()
        conn.close()
        return {'message': 'patch fund success', 'funds': list(fundList)}, 200

    def get(self, date):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        fundList = []
        for row in cursor.execute(self.select_fund_date_query, (date, )):
            fundList.append((row[0], row[1], row[2]))
        conn.commit()
        conn.close()
        return {'message': 'get fund success', 'funds': list(fundList)}, 200
