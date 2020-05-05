import requests
from bs4 import BeautifulSoup
import re
import time
from queue import Queue
import csv


queue = Queue(maxsize=10000000)
mque=Queue(maxsize=10000000)
f1 = open('官方微博用户数据.csv', encoding='UTF-8')
line = f1.readline()
while line:
	y = line
	mque.put(str(int(y)))
	line = f1.readline()
f1.close()
print('队列长度：')
print(mque.qsize())
while(not mque.empty()):
    isBerak=False
    follower_id=mque.get()
    print('解析的用户id是')
    print(follower_id)
    for Page in range(10,10000):
        queue.queue.clear()
        if (isBerak):
            break
        try:
            res = requests.get(
                'https://m.weibo.cn/api/container/getIndex?containerid=230413'+follower_id+'_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=' + str(
                    Page))
        except:
            print(u'切换ip，重新请求')
            time.sleep(2)
            res = requests.get(
                'https://m.weibo.cn/api/container/getIndex?containerid=230413'+follower_id+'_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=' + str(
                    Page))
        try:
            data = res.json()
        except:
            print(u'Json解析出错')
            time.sleep(60)
            res = requests.get(
                'https://m.weibo.cn/api/container/getIndex?containerid=230413'+follower_id+'_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=' + str(
                    Page))
            data = res.json()

        cards = data['data']['cards']
        for card in cards:
            if(card['card_type']==9):
                content_id=card['mblog']['id']
                braTime=card['mblog']['created_at']
                try:
                    braMonth=re.search(r'(\d\d)\-\d\d',braTime)        #月份
                    ccmonth=int(braMonth.group(1))
                except:
                    print('我去他妈的月份解析出错了，溜了溜了')
                    pass
                queue.put(content_id)

        try:
            if (ccmonth==4):
                print('跳4月')
                print('page:'+str(Page))
                continue
            if (ccmonth > 5):
                isBerak = True
            print('ccMonth=' + str(ccmonth))
        except:pass

        f = open('zTop100微博文本.csv', 'a', newline='', encoding="utf-8")
        csv_write = csv.writer(f)
        while(not queue.empty()):
            cont=queue.get()
            try:
                response=requests.get('https://m.weibo.cn/detail/'+cont)
            except:
                print(u'切换ip，重新请求')
                time.sleep(4)
                response = requests.get('https://m.weibo.cn/detail/' + cont)
            soup=BeautifulSoup(response.text,'lxml')
            try:
                result=soup.body.script.text
            except:
                print('script出错')
                break
            time_1=re.search(r'\"created_at\"\:\s\"(\w\w\w\s\w\w\w\s\d\d\s\d\d\:\d\d\:\d\d)\s\+\d{4}\s\d{4}\"',result)
            raw_text=re.search(r'\"text\"\:\s\"(.*)\"',result)
            text=re.sub('<[^<]+?>', '', raw_text.group(1)).replace('\n', '').strip()#去除标签
            #text=re.sub("<[^>]*>","",raw_text.group(1))
            emotion_all=re.findall('<[^<]+?>',raw_text.group(1))#获取标签
            for i in range(0,len(emotion_all)):
                emotion=re.findall("[\u4e00-\u9fa5]+", emotion_all[i])#提取标签中文
                for k in range(0,len(emotion)):
                    text+='【'+emotion[k]+'】'
            csv_write.writerow([follower_id,time_1.group(1),text])
            print(Page)
            print(follower_id)
            print(time_1.group(1))









