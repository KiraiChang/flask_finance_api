# -*- coding: utf-8 -*- 
import sqlite3
import csv
import os
import sys

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()
 
# Create table
cursor.execute('DROP TABLE IF EXISTS golds')
cursor.execute('CREATE TABLE IF NOT EXISTS golds (id INTEGER PRIMARY KEY, date text, buy real, sell real)')

insert_query = 'INSERT INTO golds VALUES(?, ?, ?, ?)'

goldList = []
for item in range(1, 9):
    path = './assets/golds/GoldPassbook201{id}.csv'.format(id= item)
    file = open(path, 'r', encoding='utf-8')
    csvCursor = csv.DictReader(file, delimiter='\t')
    for row in csvCursor:
        #print(row)
        goldList.append((None, row['日期'], row['本行買入價格'], row['本行賣出價格']))
    
    file.close()
goldList = sorted(goldList, key=lambda g: g[1])
#print(goldList)

cursor.executemany(insert_query, goldList)

select_query = 'SELECT * FROM golds'
for row in cursor.execute(select_query):
    print(row)
conn.commit()
conn.close()