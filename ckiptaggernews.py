#coding=utf8
import os, codecs
import sys
import pandas as pd
import csv
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
from pymysql import *
import numpy as np 
import json

conn = connect(host='120.126.19.100',
                    database='newstest',
                    user='remote',
                    password='gylab666', charset='utf8')
cs1 = conn.cursor()

def main():
    sql1 = "SELECT id,title FROM bingnews2 WHERE title LIKE '%驚呆%'UNION SELECT id,title FROM bingnews2 WHERE title LIKE'%爆氣%' UNION SELECT id,title FROM bingnews2 WHERE title LIKE'%網友這麼說%' UNION SELECT id,title FROM bingnews2 WHERE title LIKE'%網友這樣說%'UNION SELECT id,title FROM bingnews2 WHERE title LIKE'%網驚%'"
    cs1.execute(sql1)
    idc=[]
    title = []
    user={}
    str4=""
    alldata = cs1.fetchall()
    for s in alldata:
        idc.append(s[0])
        title.append(s[1])
    #print(len(idc))
    # Load model without GPU
    ws = WS("C:/Users/cks/Downloads/ckiptagger-master/data/data")
    pos = POS("C:/Users/cks/Downloads/ckiptagger-master/data/data")
    ner = NER("C:/Users/cks/Downloads/ckiptagger-master/data/data")

    # Create custom dictionary
    # 用讀CSV的方式讀取前面匯出的txt
    df_ner_dict = pd.read_csv(r"C:\Users\cks\Desktop\畢業專題\Python\kmeans資料分群\stop_words.txt",delimiter="\t", quoting=csv.QUOTE_NONE, header=None,encoding="utf-8")
    # 存到list
    df_ner_dict.columns = ['NER']
    list_ner_dict = list(df_ner_dict['NER'])
    dict_for_CKIP = dict((el,1) for el in list_ner_dict)
    dict_for_CKIP = construct_dictionary(dict_for_CKIP) 
    for i in range(len(title)):
        sentence_list = '朴敏英進廠「修鼻子」？最新近照曝光 網驚：有點怪怪的'#title[i]
        idh=idc[i]
        word_s = np.ravel(ws(sentence_list,coerce_dictionary=dict_for_CKIP))
        word_p = np.ravel(pos(word_s))
        pos_sentence_list = pos(word_s)
        print(word_s)
        print(word_p)
        #cs1.execute("INSERT INTO ckiptaggernews(id) VALUES ('%s')" %(idh))
        #conn.commit()
    for key, value in zip(word_s, word_p):
        user[key]=value
        jsoninfo = json.dumps(user, ensure_ascii=False)
        print(jsoninfo)
    #cs1.execute("INSERT IGNORE INTO ckiptaggernews(id,ckiptitle) VALUES ('%s','%s')" %(idh,jsoninfo))
    #conn.commit()
    print("complete")
    # Release model
    del ws
    del pos
    del ner

if __name__ == "__main__":
    main()
    #sys.exit(0)