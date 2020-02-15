import os
import sys
import csv
import pymysql


dir_711 = './store_711'
file_list = os.listdir(dir_711)
store_type = '7-11'

conn = pymysql.connect(host = '127.0.0.1', user = 'root', passwd = "123456", db = 'test', charset='utf8')
cursor = conn.cursor()

# 同步版本
for file in file_list:
    city = file.split('.')[0]

    with open(dir_711 + '/' + file, newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if '店號' in row:
                continue
            effect_row = cursor.execute(
                'INSERT INTO `convenience_store` (`type`, `city`, `store_num`, `store_name`, `address`) VALUES (%s, %s, %s, %s, %s)',
                (store_type, city, row[0], row[1], row[2])
            )

conn.commit()
cursor.close()
conn.close()