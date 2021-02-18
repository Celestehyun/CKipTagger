#coding=utf8
import os, codecs
import sys
import pandas as pd
import csv
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
from pymysql import *
import numpy as np 
import json

conn = connect(host=[your_host],
                    database=[your_db],
                    user=[db_username],
                    password=[db_password], charset='utf8')
cs1 = conn.cursor()

def main():
    sql1 = "SELECT id,title FROM bingnews2 WHERE title LIKE '%驚呆%'UNION SELECT id,title FROM bingnews2 WHERE title LIKE'%爆氣%' UNION SELECT id,title FROM bingnews2 WHERE title LIKE'%網友這麼說%' UNION SELECT id,title FROM bingnews2 WHERE title LIKE'%網友這樣說%'UNION SELECT id,title FROM bingnews2 WHERE title LIKE'%網驚%'"  
    #將資料表中部份資料抓出來，若需將資料庫中資料全部抓出來：SELECT [欄位] FROM [資料表]
    cs1.execute(sql1)
    idc=[] #id
    title = [] #標題
    user={}
    str4=""
    alldata = cs1.fetchall()
    for s in alldata:
        idc.append(s[0])
        title.append(s[1])
    #print(len(idc))
    # Load model without GPU
    ws = WS("請上CKipTagger 的github下載模型，網址詳見READ") #斷詞
    pos = POS("請上CKipTagger 的github下載模型，網址詳見READ") #詞性標註
    ner = NER("請上CKipTagger 的github下載模型，網址詳見READ") #實體辨識

    # Create custom dictionary
    # 用讀CSV的方式讀取前面匯出的txt
    df_ner_dict = pd.read_csv(r"停用詞文件儲存位置",delimiter="\t", quoting=csv.QUOTE_NONE, header=None,encoding="utf-8") #使用停用詞
    # 存到list
    df_ner_dict.columns = ['NER']
    list_ner_dict = list(df_ner_dict['NER'])
    dict_for_CKIP = dict((el,1) for el in list_ner_dict)
    dict_for_CKIP = construct_dictionary(dict_for_CKIP) 
    for i in range(len(title)):
        sentence_list = '朴敏英進廠「修鼻子」？最新近照曝光 網驚：有點怪怪的'#若修改成sentence_list = title[i]，則可以讀取資料表中所有字串
        idh=idc[i]
        word_s = np.ravel(ws(sentence_list,coerce_dictionary=dict_for_CKIP)) #斷詞
        word_p = np.ravel(pos(word_s)) #詞性標註
        pos_sentence_list = pos(word_s)
        print(word_s)
        print(word_p)

    for key, value in zip(word_s, word_p): #將斷詞結果和對應詞性以鍵值方式存為JSON檔
        user[key]=value
        jsoninfo = json.dumps(user, ensure_ascii=False)


    print("complete")
    # Release model
    del ws
    del pos
    del ner

if __name__ == "__main__":
    main()
    #sys.exit(0)
