import threading
import time
import requests
from lxml import etree
from queue import Queue

url='https://www.xsbiquge.com/'
user={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
        'Referer': 'https://www.xsbiquge.com/'}
lock=threading.Lock()
chapter={}
n=0
title_list=[]

def get_fiction_url(name):
    keyword='search.php?keyword='+name
    url_first=url+keyword
    r=requests.get(url_first,headers=user)
    html=etree.HTML(r.text)
    url_second=html.xpath('//div[@class="result-game-item-pic"]//a/@href')
    if len(url_second):
        return url_second[0]
    else:
        exit('未找到该小说')

def get_chapter_url(url_second):
    global title_list
    r=requests.get(url_second,headers=user)
    r_text=r.text
    r_text=r_text.encode('ISO-8859-1').decode('utf-8')
    html=etree.HTML(r_text)
    url_third=html.xpath('//dd//a/@href')
    title_list=html.xpath('//dd//a/text()')
    for i in range(0,len(url_third)):
        url_third[i]='https://www.xsbiquge.com'+url_third[i]
    return(url_third)

def get_text(queue):
    while queue.empty() is not True:
        r=requests.get(queue.get(),headers=user)
        r_text=r.text
        r_text=r_text.encode('ISO-8859-1').decode('utf-8')
        html=etree.HTML(r_text)
        title=html.xpath('//div[@class="bookname"]//h1/text()')
        paragraph=html.xpath('//div[@id="content"]/text()')
        lock.acquire()
        text=title[0]+'\n'
        for i in range(0,len(paragraph)):
            text=text+'    '+paragraph[i][3:]+'\n'
        text=text+'\n\n\n'
        chapter.update({title[0]:text})
        global n
        n=n+1
        print(n)
        lock.release()
        queue.task_done()

def write_text(text):
    with open('D:\DOWNLOAD\\'+name+'.txt','a+',encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    global name
    name=input('输入要下载的小说:')
    url_second=get_fiction_url(name)
    url_third=get_chapter_url(url_second)
    print('共'+str(len(url_third))+'章')
    queue=Queue()
    for i in range(0,len(url_third)):
        queue.put(url_third[i])
    for i in range(100):
        p=threading.Thread(target=get_text,args=(queue,))
        p.start()
    queue.join()
    with open('D:\DOWNLOAD\\'+name+'.txt','w+',encoding='utf-8') as f:
        f.write(name+'\n\n')
    for i in range(0,len(title_list)):
        write_text(chapter[title_list[i]])
    f.close()