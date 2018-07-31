# -*- coding: utf-8 -*- 
import sqlite3
import csv
import os
import sys

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()
 
# Create table
cursor.execute('DROP TABLE IF EXISTS exchanges')
cursor.execute('CREATE TABLE IF NOT EXISTS exchanges ('
                'id INTEGER PRIMARY KEY, '
                'date TEXT, '
                'usd_twd REAL, '
                'eur_usd REAL, '
                'gbp_usd REAL, '
                'aud_usd REAL, '
                'nzd_usd REAL)')
    # item[0].text->日期
    # item[1].text->美元／新台幣
    # item[3].text->美元／新台幣
    # item[5].text->英鎊／美元
    # item[6].text->澳幣／美元
    # item[10].text->紐幣／美元
insert_query = 'INSERT INTO exchanges VALUES(?, ?, ?, ?, ?, ?, ?)'

exchangeList = []
path = './assets/exchanges/exchange19900101.csv'
file = open(path, 'r', encoding='utf-8')
csvCursor = csv.DictReader(file, delimiter=',')
for row in csvCursor:
    #print(row)
    exchangeList.append((None, 
                            row['結束日期'], 
                            0.0 if row['USD/TWD'] == None or row['USD/TWD'] == '' else row['USD/TWD'], 
                            0.0 if row['USD/EUR'] == None or row['USD/EUR'] == ''  else 1.0 / float(row['USD/EUR']), 
                            0.0 if row['USD/GBP'] == None or row['USD/GBP'] == ''  else 1.0 / float(row['USD/GBP']), 
                            0.0 if row['USD/AUD'] == None or row['USD/AUD'] == ''  else 1.0 / float(row['USD/AUD']),
                            0.0 if row['USD/NZD'] == None or row['USD/NZD'] == ''  else 1.0 / float(row['USD/NZD'])))
    
file.close()
exchangeList = sorted(exchangeList, key=lambda g: g[1])
#print(goldList)

cursor.executemany(insert_query, exchangeList)

select_query = 'SELECT * FROM exchanges'
for row in cursor.execute(select_query):
    print(row)
conn.commit()
conn.close()