#!/usr/bin/python
import os, re
import imagecluster as ic
import common as co
import math
import gc
pj = os.path.join
import shutil


fingerPrintDir='/home/jc/codes/Projects/TBCloth/src/cluster/imgs/imagecluster'
ic_base_dir = '/home/jc/ictest'

sim = 0.4
spiltnum = 3

# I ran out ot memory because only my source finger-print file is 8.4G
# My MEM is 16G .....
# Using this script to spilt the big one to some smaller ones


def spiltFP(fpdir=fingerPrintDir,ic_base_dir = ic_base_dir,spiltnum=spiltnum):
    """
    Spilt a large finger-print file to several smaller ones
    :param fpdir: The source finger-print file direction
    :param ic_base_dir: Divided ones root location
    :param spiltnum: The num to spilt the source file
    :return: nothing
    """

    fps = co.read_pk(fpdir+'/fingerprints.pk')
    print ('total num of fingerprints : %d' % fps.__len__())

    len=fps.__len__()
    step = math.ceil(len*1.0/spiltnum)
    dicts=[{}]

    i=0
    count = 0

    for k,v in fps.items():
        dicts[i][k]=v
        count+=1
        if(count == step):
            i+=1;
            count=0
            dicts.append({})
    print ('Spilt fps in %d dicts ' % (i+1))

    i = 0
    for fpdict in dicts:
        fp_newdir = ic_base_dir+'/part'+str(i)+'/fingerprints.pk'
        print("[dict%d] has %d element writen in %s " % (i,fpdict.__len__(),fp_newdir))
        if not os.path.exists(ic_base_dir+'/part'+str(i)):
            os.makedirs(ic_base_dir+'/part'+str(i))
        co.write_pk(fpdict,fp_newdir)
        i += 1

    del fps,dicts
    gc.collect()

def linkParts( ic_base_dir = ic_base_dir , sim = sim):
    
    for dirpath, dirnames, filenames in os.walk(ic_base_dir):
        dircs = dirnames
        break
    if dircs.__len__()==0:
        print('no folder found !')
        return

    i = 0

    for f_dir in dircs:

        fpdict = co.read_pk(ic_base_dir + '/' + f_dir + '/fingerprints.pk')
        print("[dict%d] with %d is clusting " % (i, fpdict.__len__()))
        ic.make_links(ic.cluster(dict(fpdict), sim, method='average')
                      , ic_base_dir + '/part' + str(i)+'/cluster')
        i += 1

        del fpdict
        gc.collect()

def rmFiles(tar_dir = ic_base_dir):
    """
    Remove all files of this spilt folders
    :param tar_dir: Target direction for remove all children
    :return:
    """
    for dirpath, dirnames, filenames in os.walk(ic_base_dir):
        dircs = dirnames
        break
    for f_dir in dircs:
        if os.path.exists(tar_dir + '/' + f_dir):
            shutil.rmtree(tar_dir + '/' + f_dir)


spiltFP()
linkParts()