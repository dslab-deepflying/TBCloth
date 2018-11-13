#!/usr/bin/python
#-*- coding=utf-8 -*-

import pandas as pd


def main():
    itemsData = \
        pd.read_table(filepath_or_buffer='items.txt',skiprows=1,
                      header=None,sep=' ',names=['itemID','category'])
    itemCates =  itemsData['category']

    for i in [5 ,10 ,20 ,30,50,70]:
        print('sum former i :'+str(i) + ' and percentage is '+str(itemCates.value_counts()[:i].sum()*1.0/itemsData.__len__()))

    print('None count: %d in %d (%f)'%(itemCates.value_counts()['None'], itemsData.__len__(),itemCates.value_counts()['None']*1.0/itemsData.__len__()))

    # If you need a specific data of this classification
    #itemCates.value_counts().to_csv('valueCounts.txt')

main()
