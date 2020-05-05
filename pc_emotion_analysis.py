import pandas as pd
import jieba
import time


def emotion_caculate(text):
    notDic = True
    degree=1
    anger = 0
    disgust = 0
    fear = 0
    sad = 0
    surprise = 0
    good = 0
    happy = 0
    wordlist = jieba.lcut(text)
    wordset = set(wordlist)
    # wordfreq = []
    for word in wordset:
        if word =='，' or word =='。'or word =='#'or word =='【'or word =='】':
            degree = 1
            notDic = True

        if word in NotDic:
            notDic=not notDic
        if word in Degree:
            degree*=Degree_value[Degree.index(word)]

        if word in Anger:
            if notDic:
                anger += Anger_value[Anger.index(word)]*degree  #怒否定=无
            degree=1
            notDic=True

        if word in Disgust:
            if notDic:
                disgust += Disgust_value[Disgust.index(word)]*degree
            else:
                good += Disgust_value[Disgust.index(word)] * degree*0.2  #恶否定=0.2*好
            degree = 1
            notDic = True

        if word in Fear:
            if notDic:
                fear += Fear_value[Fear.index(word)]*degree    #惧否定=无
            degree = 1
            notDic = True

        if word in Sad:
            if notDic:
                sad += Sad_value[Sad.index(word)]*degree
            else:
                happy += Sad_value[Sad.index(word)]*degree*0.1   #哀否定=0.1*乐
            degree = 1
            notDic = True

        if word in Surprise:
            if notDic:
                surprise += Surprise_value[Surprise.index(word)]*degree    #惊否定=无
            degree = 1
            notDic = True

        if word in Happy:
            if notDic:
                happy += Happy_value[Happy.index(word)]*degree
            else:
                sad += Happy_value[Happy.index(word)]*degree   #哀否定=乐
            degree = 1
            notDic = True

        if word in Good:
            if notDic:
                good += Good_value[Good.index(word)]*degree
            else:
                disgust += Good_value[Good.index(word)]*degree #好否定=恶
            degree = 1
            notDic = True

    emotion_info = {
        'length': len(wordlist),
        'happy': happy,
        'good': good,
        'surprise': surprise,
        'sadness': sad,
        'fear': fear,
        'anger': anger,
        'disgust': disgust,
    }
    indexs = ['length','happy','good','surprise','sadness','fear','anger','disgust']
    return pd.Series(emotion_info, index=indexs)


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
    print('情绪词语列表整理完成')

    weibo_df = pd.read_csv('田园博主微博文本.csv', encoding='utf-8',error_bad_lines=False).astype(str)
    start = time.time()
    emotion_df = weibo_df['review'].apply(emotion_caculate)
    end = time.time()
    print(end - start)
    print(emotion_df.head())
    output_df = pd.concat([weibo_df, emotion_df], axis=1)
    output_df.to_csv('田园博主情感分析结果.csv', index=False)
    output_df.head()


