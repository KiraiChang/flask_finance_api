# -*- coding: utf-8 -*- 
import sqlite3
import csv
import os
import sys

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()
 
# Create table
cursor.execute('DROP TABLE IF EXISTS stocks')
cursor.execute('CREATE TABLE IF NOT EXISTS stocks ('
                'id INTEGER PRIMARY KEY, '
                'date TEXT, '
                'open_price REAL, '
                'max_price REAL, '
                'min_price REAL, '
                'close_price REAL, '
                'decline REAL, ' 
                'volume INTEGER, '
                'amount INTEGER)')
    #item[0].text->日期
    #item[3].text->開盤價
    #item[4].text->最高價
    #item[5].text->最低價
    #item[6].text->收盤價
    #item[7].text->漲跌價差
    #item[1].text->成交股數
    #item[2].text->成交金額
    #item[8].text->成交筆數
insert_query = 'INSERT INTO stocks VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'

stockList = []
for item in range(1, 9):
    path = './assets/stock/201{id}-0050.csv'.format(id= item)
    file = open(path, 'r', encoding='utf-8')
    csvCursor = csv.DictReader(file, delimiter='\t')
    for row in csvCursor:
        #print(row)
        stockList.append((None, row['日期'], row['開盤'], row['最高'], row['最低'], row['收盤'], row['漲跌'], row['成交量'], row['成交金額']))
    
    file.close()
stockList = sorted(stockList, key=lambda g: g[1])
#print(goldList)

cursor.executemany(insert_query, stockList)

select_query = 'SELECT * FROM stocks'
for row in cursor.execute(select_query):
    print(row)
conn.commit()
conn.close()