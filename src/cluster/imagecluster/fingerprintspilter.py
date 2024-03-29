#!/usr/bin/python
import os, re
import imagecluster as ic
import common as co
import math
import random
import gc
import shutil
import argparse
pj = os.path.join

fingerPrintDir='/home/deepcam/ictest'
ic_base_dir= '/home/deepcam/ictest'


sim = 0.4

# Round step length
stepNum = 30000

# I ran out ot memory because only my source finger-print file is 8.4G
# My MEM is 16G .....
# Using this script to spilt the big one to some smaller ones


def spiltFP(fpdir=fingerPrintDir,ic_base_dir = ic_base_dir):
    """
    Spilt a large finger-print file to several smaller ones
    :param fpdir: The source finger-print file direction
    :param ic_base_dir: Divided ones root location
    :param spiltnum: The num to spilt the source file
    :return: nothing
    """

    fps = co.read_pk(fpdir+'/fingerprints.pk')
    print ('total num of fingerprints : %d' % fps.__len__())

    step = stepNum  # Pre-set step

    len=fps.__len__()
    spiltnum = len/step

    if spiltnum > 1 and (len - step*(spiltnum-1)) < step/2:
        spiltnum -= 1

    step = math.ceil(len*1.0/spiltnum)

    dicts = [{}]

    i = 0
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


def linkParts( ic_base_dir = ic_base_dir , sim = sim):
    """
    Link all divided part by each divided finger-print
    :param ic_base_dir:
    :param sim:
    :return:
    """
    for dirpath, dirnames, filenames in os.walk(ic_base_dir):
        dircs = dirnames
        break
    if dircs.__len__() == 0:
        print('Try to link images , no former folder found !')
        spiltFP(fpdir=fingerPrintDir,ic_base_dir=ic_base_dir)
        for dirpath, dirnames, filenames in os.walk(ic_base_dir):
            dircs = dirnames
            break
    i = 0
    for f_dir in dircs:
        fpdict = co.read_pk(ic_base_dir + '/' + f_dir + '/fingerprints.pk')
        print("[dict%d] with %d is clusting [sim=%f]" % (i, fpdict.__len__(),sim))
        ic.make_links(ic.cluster(dict(fpdict), sim, method='average')
                      , ic_base_dir + '/part' + str(i)+'/cluster')
        i += 1

        del fpdict


def linkTest( ic_base_dir = ic_base_dir , sim = sim):
    """
    Random link a divided part by its divided finger-print
    :param ic_base_dir:
    :param sim:
    :return:
    """
    for dirpath, dirnames, filenames in os.walk(ic_base_dir):
        dircs = dirnames
        break
    if dircs.__len__()==0:
        print('no former folder found !')
        spiltFP()

    print ('Link test')

    f_dir = dircs[random.randint(0,dircs.__len__()-1)]
    fpdict = co.read_pk(ic_base_dir + '/' + f_dir + '/fingerprints.pk')
    print("[%s] with %d is clusting " % (f_dir, fpdict.__len__()))
    ic.make_links(ic.cluster(dict(fpdict), sim, method='average')
                    , ic_base_dir + '/' + f_dir+'/cluster')

    del fpdict
    gc.collect()

def rmFiles(tar_dir = ic_base_dir,rmAll = False):
    """
    Remove all files of this spilt folders
    :param tar_dir: Target direction for remove all children
    :param rmAll: 'False':remove cluster result only
    :return:
    """
    for dirpath, dirnames, filenames in os.walk(ic_base_dir):
        dircs = dirnames
        break


    for f_dir in dircs:
        if rmAll and os.path.exists(tar_dir + '/' + f_dir):
            shutil.rmtree(tar_dir + '/' + f_dir)
        if (not rmAll) and os.path.exists(tar_dir + '/' + f_dir+'/cluster'):
            shutil.rmtree(tar_dir + '/' + f_dir + '/cluster')


def main(_cmd,_fingerPrintDir,_ic_base_dir,_sim=sim,_rmfile=''):

    global sim,fingerPrintDir,ic_base_dir

    sim = _sim
    fingerPrintDir = _fingerPrintDir
    ic_base_dir = _ic_base_dir

    if _cmd == 'Cluster':
        if _rmfile == 'all':
            rmFiles(rmAll=True)
        elif _rmfile == 'result':
            rmFiles(rmAll=False)
        linkParts(ic_base_dir=ic_base_dir, sim=sim)
    elif _cmd =='Spilt':
        spiltFP(fpdir=fingerPrintDir,ic_base_dir=ic_base_dir)
    else:
        linkTest()


if __name__ == 'main' or __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=' Spilt large finger-print to several smaller one ; Test or clean them ',
        formatter_class= argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('cmd',choices=['Cluster','Spilt','Test'],help='Cluster it by splilting ; Just spilt ;'
                                                                      ' Test a divided fp ' )

    parser.add_argument('--sim',default=sim,
                        help='similarity or each element 0..1')

    parser.add_argument('--rmFile',choices=['all','result','none'],default='result',
                        help= 'Only work by \'Cluster\' , Remove divided finger-print and result ')

    args = parser.parse_args()

    sim = args.sim

    cmd = args.cmd

    rmFile = cmd.rmFile

    main(_sim=sim,_cmd=cmd,_rmfile=rmFile)


#246634
#fps = co.read_pk(fingerPrintDir+'/fingerprints.pk')
#print ('total num of fingerprints : %d' % fps.__len__())