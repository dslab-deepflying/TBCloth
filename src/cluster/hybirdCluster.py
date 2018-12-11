#!/usr/bin/python
import pandas as pd
import sys
from imagecluster import common as co
from imagecluster import imagecluster as ic
from tools import resultFilter
import os
import shutil

classifier_result_path = '/home/deepcam/Data/tbcloth/result.txt'
img_folder_path = '/home/deepcam/Data/tbcloth/imgs/'
full_fp_path = '/home/deepcam/Data/fp/inceptionv3/fingerprints.pk'
sampled_fp_path = '/home/deepcam/Data/fp/sampled/fingerprints.pk'
converted_txt_path = '/home/deepcam/Data/tbcloth/tee.txt'
ic_base_dir = '/home/deepcam/Data/tbcloth/hybridCluster'


def get_result():
    result_DF = pd.read_csv(classifier_result_path,
                            header=None)
    i=0
    max_num=result_DF.shape[0]
    res_arr = []

    for i in range(max_num):
        if str(result_DF[1][i][1:]).split(':')[0] == 'tee':
            res_arr.append(img_folder_path+str(result_DF[0][i]).split('/')[4])
    pd.Series(res_arr).to_csv(converted_txt_path,index=None)
#26709

def get_fp():

    fp = dict(co.read_pk(full_fp_path))
    new_dic = {}
    print fp.keys()[0:5]
    result_list = pd.read_csv(converted_txt_path,
                            header=None)[0]
    i = 0
    num = result_list.__len__()

    for res in result_list:
        i += 1
        new_dic[res] = fp[res]
        sys.stdout.write('\r[%.2f%%]' % (i * 100.0 / num))
        sys.stdout.flush()

    print ('\n')
    co.write_pk(new_dic,sampled_fp_path)

def link_parts( ic_base_dir = ic_base_dir, sim = 0.55 ) :

    for dirpath, dirnames, filenames in os.walk(ic_base_dir):
        dircs = dirnames
        break

    for dirc in dircs:
        shutil.rmtree(ic_base_dir+'/'+dirc)

    fpdict = co.read_pk(sampled_fp_path)

    print("Dict has  %d is clusting [sim=%f]" % (fpdict.__len__(), sim))
    ic.make_links(ic.cluster(dict(fpdict), sim, method='average')
                   , ic_base_dir + '/cluster')

    # resultFilter.filter_folder(ic_base_dir,total_num=fpdict.__len__(),img_folder=img_folder_path)

    del fpdict


link_parts()