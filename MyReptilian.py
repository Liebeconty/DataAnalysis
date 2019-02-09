import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor

start = time.clock()

plist = [] # 为1-100页的URL的编号num
for i  in range(1,101):
    j = 44*(i-1)
    plist.append(j)

listno = plist
datatmsp = pd.DataFrame(columns = [])

while True:
    @retry(stop_max_attempt_number = 8)
    def network_programming(num):
        url = 'https://s.taobao.com/search?q=%E6%B2%99%E5%8 \
        F%91&imgfile=&js=1&stats_click=search_radio_all%3 \
        A1&initiative_id=staobaoz_20180610&ie=utf8&sort= \
        sale-desc&style=list&fs=1&filter_tianmao=tmall& \
        filter=reserve_price%5B500%2C%5D&bcoffset-0 \
        &p4ppushleft-%2C44&s=' + str(num)
        web = requests.get(url,headers = headers)
        web.encoding = 'utf-8'
        return web
#   多线程
    def multithreading():
        number = listno
        event = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            for result in executor.map(network_programming,number,chunksize=10):
                event.append(result)
        return event
#   隐藏修改headers参数
    headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit \
               /537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 \
               Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13059.400'}

    listpg = []
    event = multithreading()
    for i in event:
        json = re.findall('"auctions":(.*?),"recommendAuctions"',i.text)
        if len(json):
            table = pd.read_json(json[0])
            datatmsp = pd.concat([datatmsp,table],
                                 axis = 0,ignore_index=True)
            pg = re.findall('"pageNum":(.*?),"p4pbottom_up"',i.text)[0]
            listpg.append(pg)

    lists = []
    for a in listpg:
        b = 44*(int(a)-1)
        lists.append(b)

    listn = listno
    listno = []
    for p in listn:
        if p not in lists:
            listno.append(p)

    if len(listno) == 0:
        break

datatmsp.to_excel('datatmsp2.xls',index=False)
end = time.clock()
print("爬取完成 用时：",end - start,'s')
    
