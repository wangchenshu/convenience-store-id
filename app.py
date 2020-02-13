#!/usr/bin/env python

import os
import sys
import csv
import time
import requests
from bs4 import BeautifulSoup

# import concurrent.futures
import asyncio

def check_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def save_store_data(data):
    save_dir = data['save_dir']
    city = data['city']
    url = data['url']
    myobj = {'strTargetField': 'COUNTY', 'strKeyWords': city}
    res = requests.post(url, data=myobj, headers=headers)
    data_soup = BeautifulSoup(res.text, 'html.parser')

    tr_tags = data_soup.find_all("tr")
    with open(save_dir + '/' + city + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for tr in tr_tags:
            data = tr.text.split()
            if len(data) > 2:
                writer.writerow([data[0], data[1], data[2]])

async def save_store_data_async(data):
    res = await loop.run_in_executor(None, save_store_data, data)

headers = {
    'user-agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Cookie': '_ga=GA1.3.710486409.1581597245; _gid=GA1.3.874113313.1581597245',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
}
index_url_ibon = 'https://www.ibon.com.tw/'
post_url_ibon = index_url_ibon + 'retail_inquiry_ajax.aspx'
dir_711 = './store_711'
citys = [
    "台北市",
    "新北市",
    "基隆市",
    "宜蘭縣",
    "桃園市",
    "新竹市",
    "新竹縣",
    "苗栗縣",
    "台中市",
    "彰化縣",
    "南投縣",
    "雲林縣",
    "嘉義市",
    "嘉義縣",
    "台南市",
    "高雄市",
    "屏東縣",
    "花蓮縣",
    "台東縣",
    "澎湖縣",
    "金門縣",
    "連江縣",
    "南海諸島"
]

## 建立資料夾
check_dir(dir_711)

## 7-11
## 同步版本
# for city in citys:
#     data = {
#         'save_dir': dir_711,
#         'city': city,
#         'url': post_url_ibon
#     }
#     save_store_data(data)
#     time.sleep(0.2)

# 異步版本
tasks = []
loop = asyncio.get_event_loop()

for city in citys:
    data = {
        'save_dir': dir_711,
        'city': city,
        'url': post_url_ibon
    }
    task = loop.create_task(save_store_data_async(data))
    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))
