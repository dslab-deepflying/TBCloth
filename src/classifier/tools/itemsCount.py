#!/usr/bin/python
#-*- coding=utf-8 -*-

import pandas as pd


def main():
    itemsData = \
        pd.read_table(filepath_or_buffer='items.txt',skiprows=1,
                      header=None,sep=' ',names=['itemID','category'])
    itemCates =  itemsData['category']

    print(itemCates.sort_values().value_counts().sum())

main()