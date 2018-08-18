# -*- coding: utf-8 -*-
import sqlite3
import csv

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Create table
cursor.execute('DROP TABLE IF EXISTS funds')
cursor.execute(
    'CREATE TABLE IF NOT EXISTS funds'
    ' (id INTEGER PRIMARY KEY, date text, price real)'
)

insert_query = 'INSERT INTO funds VALUES(?, ?, ?)'

fundList = []
path = './assets/funds/ALB04USD.csv'
file = open(path, 'r', encoding='utf-8')
csvCursor = csv.DictReader(file, delimiter='\t')
for row in csvCursor:
    # print(row)
    fundList.append((None, row['日期'], row['淨值']))

file.close()
fundList = sorted(fundList, key=lambda g: g[1])

cursor.executemany(insert_query, fundList)

select_query = 'SELECT * FROM funds'
for row in cursor.execute(select_query):
    print(row)
conn.commit()
conn.close()
