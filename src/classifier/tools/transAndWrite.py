#!/usr/bin/python3
#-*- coding: utf-8 -*-
import pandas as pd
from translate import Translator
translator= Translator(to_lang="zh")

l1 = pd.read_csv('cateCount.txt',skiprows=0)['cate']
l2 = []
for i in range(100):
    print("Correct ? %s to %s %d" %(str(l1[i]),translator.translate(str(l1[i]).replace('_',' ')),i+1))
    content = raw_input()
    if (content == 'q'):
        break
    elif (content == 'y' or content == 'Y'):
        l2.append(l1[i])
    i+=1
    print('\t')
l2=pd.Series(l2).to_csv('cates.txt')
