import threading
import time
import requests
from lxml import etree
from queue import Queue
import os.path

url = 'https://www.mn5.cc/Mtcos/'
user = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40",
    'Referer': 'https://www.mn5.cc/Xiuren/'}
proxies = {
    'http': 'http://165.225.72.66:10605',
}
lock = threading.Lock()


def get_pictures_url(page):
    global title
    if page == 1:
        url_first = url
    elif page > 1:
        url_first = url + 'page_' + str(page) + '.html'
    r = requests.get(url_first, headers=user)
    r_text = r.text
    r_text = r_text.encode('ISO-8859-1').decode('GBk')
    html = etree.HTML(r_text)
    url_second = html.xpath('//div[@class="biank1"]//a/@href')
    title = html.xpath('//div[@class="biank1"]//a//img/@title')
    for i in range(0, len(url_second)):
        url_second[i] = 'https://www.mn5.cc' + url_second[i]
    return url_second


def get_page_url(url_second):
    r = requests.get(url_second, headers=user)
    html = etree.HTML(r.text)
    url_third = html.xpath('//div[@class="page"]//a/@href')
    url_third = de_weight(url_third)
    return url_third


def de_weight(url_third):
    url_third_two = []
    for i in url_third:
        i = 'https://www.mn5.cc' + i
        if i not in url_third_two:
            url_third_two.append(i)
    return url_third_two


def get_picture_url(url_third):
    print('正在获取图片下载列表')
    global url_fifth
    global url_key_two
    queue = Queue()
    queue_two = Queue()
    url_fourth = []
    url_fifth = []
    url_key_two = {}
    for i in range(0, len(url_third)):
        queue_two.put(url_third[i])
    for i in range(16):
        p = threading.Thread(target=get_picture_url_two, args=(queue_two,))
        p.start()
    queue_two.join()
    for i in range(0, len(url_third)):
        url_fourth = url_key_two[url_third[i]]
        for j in range(0, len(url_fourth)):
            queue.put('https://p4.plmn5.com//u' + url_fourth[j][2:])
            url_fifth.append('https://p4.plmn5.com//u' + url_fourth[j][2:])
    for i in range(0, len(url_fifth)):
        url_key.update({url_fifth[i]: i})
    return queue


def get_picture_url_two(queue_two):
    global url_key_two
    global n
    while queue_two.empty() is not True:
        try:
            x = queue_two.get()
            r = requests.get(x, headers=user, proxies=proxies, timeout=5)
            html = etree.HTML(r.text)
            url_fourth = html.xpath('//img[@onload="size(this)"]/@src')
            url_key_two.update({x: url_fourth})
            queue_two.task_done()
        except:
            queue_two.task_done()
            n = n + 1


def get_picture(queue, i):
    global url_key
    global n
    while queue.empty() is not True:
        try:
            x = queue.get()
            print(x)
            y = url_key[x]
            r = requests.get(x, headers=user, proxies=proxies, timeout=5)
            with open('D:\PICTURE\写真\\' + title[i] + '\\' + str(y + 1) + '.jpg', 'wb') as f:
                f.write(r.content)
                f.close()
            print(x)
            queue.task_done()
        except:
            queue.task_done()
            n = n + 1


if __name__ == "__main__":
    global title
    global url_key
    global url_key_two
    global n
    n = 0
    title = []
    url_key = {}
    queue = Queue()
    page = input('输入要爬取的页数:')
    url_second = get_pictures_url(int(page))
    for i in range(20):
        print('▪▪▪▪▪▪▪▪▪▪' + title[i] + '▪▪▪▪▪▪▪▪▪▪')
        url_key.clear()
        url_third = get_page_url(url_second[i])
        queue = get_picture_url(url_third)
        if not os.path.isdir('D:\PICTURE\写真\\' + title[i]):
            os.makedirs('D:\PICTURE\写真\\' + title[i])
        for j in range(10):
            p = threading.Thread(target=get_picture, args=(queue, i,))
            p.start()
        queue.join()
    print('完成,共出现' + str(n) + '处错误')
