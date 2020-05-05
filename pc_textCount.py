import pandas as pd
import jieba
import time
import csv
'''
词频统计
'''

if __name__ == '__main__':
    df = pd.read_excel('大连理工大学中文情感词汇本体.xlsx')

    df = df[['词语', '词性种类', '词义数', '词义序号', '情感分类', '强度', '极性']]
    print(df.head())
    df_n=pd.read_excel('notDic.xlsx')
    print(df_n.head())
    df_d=pd.read_excel('degree.xlsx')
    print(df_d.head())

    NotDic = []
    Degree=[]
    Degree_value=[]
    Happy = []      #乐
    Happy_value=[]
    Good = []       #好
    Good_value = []
    Surprise = []       #惊
    Surprise_value = []
    Anger = []      #怒
    Anger_value = []
    Sad = []        #哀
    Sad_value = []
    Fear = []       #惧
    Fear_value = []
    Disgust = []        #恶
    Disgust_value = []
    for idx, row in df_n.iterrows():
        NotDic.append(row['否定词'])
    print('否定词表整理完成')
    for idx, row in df_d.iterrows():
        Degree.append(row['副词'])
        Degree_value.append(row['权重'])
    print('程度副词词表整理完成')


    for idx, row in df.iterrows():
        if row['情感分类'] in ['PA', 'PE']:
            Happy.append(row['词语'])
            Happy_value.append(row['强度'])
        if row['情感分类'] in ['PD', 'PH', 'PG', 'PB', 'PK']:
            Good.append(row['词语'])
            Good_value.append(row['强度'])
        if row['情感分类'] in ['PC']:
            Surprise.append(row['词语'])
            Surprise_value.append(row['强度'])
        if row['情感分类'] in ['NA']:
            Anger.append(row['词语'])
            Anger_value.append(row['强度'])
        if row['情感分类'] in ['NB', 'NJ', 'NH', 'PF']:
            Sad.append(row['词语'])
            Sad_value.append(row['强度'])
        if row['情感分类'] in ['NI', 'NC', 'NG']:
            Fear.append(row['词语'])
            Fear_value.append(row['强度'])
        if row['情感分类'] in ['NE', 'ND', 'NN', 'NK', 'NL']:
            Disgust.append(row['词语'])
            Disgust_value.append(row['强度'])
    emo = Happy + Good + Surprise + Anger + Sad + Fear + Disgust
    print('情绪词语列表整理完成')

    weibo_df = pd.read_csv('情感博主微博文本.csv', encoding='utf-8').astype(str)
    w_df = pd.read_csv('人民日报微博文本.csv', encoding='utf-8').astype(str)
    Li=[]
    LI_count=[]

    for idx, row in weibo_df.iterrows():
        wordlist = jieba.lcut(row['review'])
        wordset = set(wordlist)
        for word in wordset:
            if word not in emo and word not in NotDic and word not in Degree:
                if word in Li:
                    LI_count[Li.index(word)]+=1
                else:
                    Li.append(word)
                    LI_count.append(1)
    print('weibo_df finish')
    for idx, row in w_df.iterrows():
        wordlist = jieba.lcut(row['review'])
        wordset = set(wordlist)
        for word in wordset:
            if word not in emo and word not in NotDic and word not in Degree:
                if word in Li:
                    LI_count[Li.index(word)] += 1
                else:
                    Li.append(word)
                    LI_count.append(1)
    print('w_df finish')
    print(len(Li))
    f = open('词频统计.txt', 'a', newline='', encoding="utf-8")
    csv_write = csv.writer(f)
    for i in range(len(Li)):
      csv_write.writerow([Li[i], LI_count[i]])


