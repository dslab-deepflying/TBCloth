#! /usr/bin/python

import os,sys,shutil
import pandas as pd

min_amount = 8
max_amount = 700
total_num = 498823

#base_dir='/home/jc/deepcam/ictest' #server
base_dir='/home/deepcam/ictest'
iterate_dir='/home/deepcam/'


def main():
    parts = []
    for dirpath, dirnames, filenames in os.walk(base_dir):
        parts = dirnames
        break

    file_list = []

    for dirname in parts:

        part_path = base_dir+'/'+dirname+'/cluster/'

        for dirpath, dirnames, filenames in os.walk(part_path):
            folders = dirnames
            break

        tars = []
        sec_tars=[]


        for folder in folders:
            if folder == 'none':
                tars.append('none')
            elif int(folder.split('_')[2]) > max_amount :
                print folder
                tars.append(folder)
            elif int(folder.split('_')[2]) < min_amount :
                print folder
                sec_tars.append(folder)

    # Count folders which contain enormous big amounts of images
        for tar in tars:
            for dirpath, dirnames, filenames in os.walk(part_path+tar+'/cluster_0'):
                file_list = file_list + filenames
                print file_list.__len__()
                break

    # Count folders which contain images that small patch but large num
        for tar in sec_tars:
            for dirpath, dirnames, filenames in os.walk(part_path+tar):
                for dir in dirnames:
                    for dirpath, dirnames, filenames in os.walk(part_path + tar + dir):
                        file_list = file_list + filenames
                        print file_list.__len__()
                        break

        pd.Series(file_list).to_csv(base_dir+'/nones.txt',index=False)

def count_num():
    s1 = pd.read_csv(base_dir+'/nones.txt')
    print ('\n meaning less imgs count : %d ,about [%d%%]' %(s1.__len__(),int(s1.__len__()*1.0/total_num*100)))

if __name__ == 'main' or __name__ == '__main__':
    main()
    count_num()
