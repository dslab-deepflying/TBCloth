#! /usr/bin/python

import os,sys,shutil
import pandas as pd
import re, pickle, os

max_group = 10

max_amount = 700

total_num = 498823

#base_dir='/home/jc/deepcam/ictest' #server
base_dir='/home/deepcam/IRoot'

def handle_all(base_dir = base_dir):
    iter_folders = []
    part_folders = []
    group_folders = []
    imgs = []
    results = []

    sum = 0

    for dirpath, dirnames, filenames in os.walk(base_dir):
        iter_folders = dirnames
        break

    for iter_folder in iter_folders :
        # if iter_folder == 'iter0':
        #     fpf_path = '/home/deepcam/Data/fp/inceptionv3'
        # else:
        #     fpf_path = base_dir+'/'+iter_folder+'/fingerprints'

        # fp = read_pk(fpf_path)

        for dirpath, dirnames, filenames in os.walk(base_dir+'/'+iter_folder):
            part_folders = dirnames
            break

        for part_folder in part_folders:
            for dirpath, dirnames, filenames in os.walk(base_dir + '/' + iter_folder+'/'+part_folder+'/cluster'):
                group_folders = dirnames
                break
            sum += group_folders.__len__()

    print ('Total manual cost : %d ' % sum)

def filter_folder(path_name = base_dir,total_num=total_num , img_folder = ''):

    path_name += '/cluster'
    folders = []
    file_list = []
    for dirpath, dirnames, filenames in os.walk(path_name):
        folders = dirnames
        break

    # One kind of useless cluster result:
    # (1) no similar imgs which named 'none'
    # (2) similar imgs in one group which more than a limit
    # **(2)** is a Empirical Regular in this data-set
    tars = []

    # Another kind of useless cluster result:
    # cluster result has much group that can't be handle manually
    sec_tars = []

    if folders.__len__() == 0:
        return

    for folder in folders:
        if folder == 'none':
            tars.append('none')
        elif folder == 'meaningless':
            shutil.rmtree(path_name+'/meaningless')
        elif int(folder.split('_')[2]) > max_amount:
            tars.append(folder)

        else:
            for dirpath, dirnames, filenames in os.walk(path_name + '/' + folder):
                if dirnames.__len__() > max_group:
                    sec_tars.append(folder)
                break

    # Count folders which contain enormous big amounts of images
    for tar in tars:
        for dirpath, dirnames, filenames in os.walk(path_name + '/' + tar + '/cluster_0'):
            file_list = file_list + filenames
            break
        #shutil.rmtree(path_name + '/' + tar)

    # Count folders which contain images that small patch but large num
    for tar in sec_tars:
        for dirpath, dirnames, filenames in os.walk(path_name + '/' + tar):
            for dir in dirnames:
                for dirpath, dirnames, filenames in os.walk(path_name + '/' + tar + '/' + dir):
                    file_list = file_list + filenames
                    break
        # shutil.rmtree(path_name + '/' + tar)


    os.mkdir(path_name+'/meaningless')

    for fi in file_list:
        os.symlink(img_folder + '/' + fi , path_name + '/meaningless/'+fi)

    pd.Series(file_list).to_csv(path_name + '/nones.txt', index=False)
    print ('\n meaning less imgs count : %d ,about [%.2f%%]' % (file_list.__len__()
                                                            , file_list.__len__() * 1.0 / total_num * 100))


def main(base_dir = base_dir,total_num=total_num):
    parts = []
    for dirpath, dirnames, filenames in os.walk(base_dir):
        parts = dirnames
        break

    file_list = []

    for dirname in parts:

        part_path = base_dir+'/'+dirname+'/cluster'

        folders = []
        for dirpath, dirnames, filenames in os.walk(part_path):
            folders = dirnames
            break

        # One kind of useless cluster result:
        # (1) no similar imgs which named 'none'
        # (2) similar imgs in one group which more than a limit
        # **(2)** is a Empirical Regular in this data-set
        tars = []

        # Another kind of useless cluster result:
        # cluster result has much group that can't be handle manually
        sec_tars=[]

        if folders.__len__()==0:
            continue

        for folder in folders:
            if folder == 'none':
                tars.append('none')

            elif int(folder.split('_')[2]) > max_amount:
                tars.append(folder)

            else:
                for dirpath, dirnames, filenames in os.walk(part_path + '/' +folder):
                    if dirnames.__len__() > max_group:
                        sec_tars.append(folder)
                    break



        # Count folders which contain enormous big amounts of images
        for tar in tars:
            for dirpath, dirnames, filenames in os.walk(part_path + '/' + tar + '/cluster_0'):
                file_list = file_list + filenames
                break
            shutil.rmtree(part_path + '/' + tar)

        # Count folders which contain images that small patch but large num
        for tar in sec_tars:
            for dirpath, dirnames, filenames in os.walk(part_path + '/' + tar):
                for dir in dirnames:
                    for dirpath, dirnames, filenames in os.walk(part_path + '/' + tar + '/' + dir):
                        file_list = file_list + filenames
                        break
            shutil.rmtree(part_path + '/' + tar)

    pd.Series(file_list).to_csv(base_dir + '/nones.txt', index=False)
    print ('\n meaning less imgs count : %d ,about [%.2f%%]' % (file_list.__len__()
                                    , file_list.__len__() * 1.0 / total_num * 100))

def read_pk(fn):
    with open(fn, 'rb') as fd:
        ret = pickle.load(fd)
    return ret

def write_pk(obj, fn):
    with open(fn, 'wb') as fd:
        pickle.dump(obj, fd)


if __name__ == 'main' or __name__ == '__main__':
    handle_all()

