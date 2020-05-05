import requests
import json
import pymysql
import time
from queue import Queue

#爬虫队列
queue_scrapy = Queue(maxsize=10000000)

# 打开数据库连接
coon = pymysql.connect("localhost", "root", "root", "biyelunwen")

# 使用cursor()方法获取操作游标
cursor = coon.cursor()

FOLLOWERS='1779227543'
queue_scrapy.put(FOLLOWERS)

while(not queue_scrapy.empty()):
    next_follower_id=queue_scrapy.get()
    time.sleep(2)
    print('关注者id：'+next_follower_id)
    for Page in range(1,11):
        try:
            response=requests.get('https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_'+next_follower_id+'&page='+str(Page))
        except:
             print(u'切换ip，重新请求')
             time.sleep(4)
             response = requests.get('https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_' + next_follower_id + '&page=' +str(Page))
        try:
            data = response.json()
        except:
            print(u'Json解析出错')
            time.sleep(2)
            break

        cards=data['data']['cards']

        # pprint.pprint(cards)
        for card in cards:
             users=card['card_group']

             for user in users:
                 if(user['card_type']==10):
                     user_de=user['user']
                     user_de_id=str(user_de['id'])
                     user_de_screen_name=user_de['screen_name']
                     user_de_profile_url=user_de['profile_url']
                     #筛选出微博名不含微博两字的用户
                     if(user_de_screen_name.find(u'微博')==-1):

                         # SQL 插入语句
                         sql = "INSERT INTO follower_1 VALUES ('%s', '%s', '%s', '%s')" \
                               % (next_follower_id,user_de_id,user_de_screen_name,user_de_profile_url)
                         try:
                             # 执行sql语句
                             cursor.execute(sql)
                             # 提交到数据库执行
                             coon.commit()
                             #进入队列
                             queue_scrapy.put(user_de_id)
                             print(user_de_id)
                             print(user_de_screen_name)
                             print(user_de_profile_url)
                             print(time.strftime('%H:%M:%S',time.localtime(time.time())))
                         except:
                             # 如果发生错误则回滚
                             coon.rollback()
                         # print(user_de['id'])
                         # print(user_de['screen_name'])
                         # print(user_de['profile_url'])
# 关闭数据库连接
coon.close()