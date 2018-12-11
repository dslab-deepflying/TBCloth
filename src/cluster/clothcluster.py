import os,sys
import shutil
import re
import argparse
import random

from imagecluster import common as co
import pandas as pd

#from src.cluster.imagecluster import main  # use pycharm run
from imagecluster import main as cluster # use python command line
from imagecluster import fingerprintspilter
from tools import resultFilter


iterCount = 0
sim = 0.7

# iterate_root_path = '/home/jc/IRoot'
iterate_root_path = '/home/deepcam/IRoot'

fpf_path = '/home/deepcam/Data/fp/inceptionv3'#fp/inceptionv3

imagedir = '/home/deepcam/Data/tbcloth/imgs'

def get_iter_fp(txt_path,save_path,formerFP_path):

    txt_path += '/nones.txt'
    formerFP_path += '/fingerprints.pk'

    files = pd.read_csv(txt_path,header=None,index_col=None)
    files = list(files[0])

    random.shuffle(files)
    random.shuffle(files)

    print ('nones.txt contain %d ' % files.__len__())
    fpdict = co.read_pk(formerFP_path)
    print ('former fingerprints contain %d ' % len(fpdict))
    newdict={}
    for fname in files:
        tkey = imagedir+'/'+fname
        newdict[tkey] = fpdict[tkey]
    co.write_pk(newdict, save_path+'/fingerprints.pk')

# get_iter_fp(txt_path='/home/deepcam/ictest/nones.txt'
#             , save_path='/home/deepcam/IRoot',
#             formerFP_path='/home/deepcam/Data/fp')


def get_former_iter(iterate_root_path=iterate_root_path):

    i = 0

    for dirpath, dirnames, filenames in os.walk(iterate_root_path):
        for dirname in dirnames:
            if re.match('iter\d+', dirname) != None and os.path.exists(iterate_root_path+'/'+dirname+'/nones.txt') :
                i += 1
        break
    return  i

def main(iterCount):

    if not os.path.exists(fpf_path+'/fingerprints.pk'):
        print (fpf_path+' no fp found , creating ')
        cluster.get_fp(imagedir=imagedir, ic_base_dir=fpf_path)

    if iterCount == 0:
        print('No iterate , clustering ')

        # cluster.main(imagedir=imagedir,ic_base_dir=fpf_path)
        fingerprintspilter.main(_cmd='Cluster',_fingerPrintDir=fpf_path,
                                _ic_base_dir=iterate_root_path,_sim=sim,_rmfile='result')
    elif iterCount > 0:

        print('Iterated clustering ')

        # If we have no fp exists , then get one
        if not os.path.exists(fpf_path+'/fingerprints.pk'):
            cluster.get_fp(imagedir=imagedir,ic_base_dir=fpf_path)

        # # Delete former results by iterating
        # for dirpath, dirnames, filenames in os.walk(iterate_root_path):
        #     for dirname in dirnames:
        #         if re.match('iter\d+',dirname) != None:
        #             shutil.rmtree(iterate_root_path+'/'+dirname)
        #     break

        former_count = get_former_iter(iterate_root_path=iterate_root_path)

        for count in range(former_count,iterCount):

            folderName = iterate_root_path+'/iter'+str(count)
            if not os.path.exists(folderName):
                os.makedirs(folderName)

            print ('Iter %d \n' % count)

            # Step 1: Find fingerprints and cluster

            if count == 0:

                # Step 1.a.1 : Auto-Cluster
                # If the mount of imgs is large , it will be automatically divided
                # into some smaller task to do
                fingerprintspilter.main(_sim=sim,_cmd='Cluster',_fingerPrintDir=fpf_path
                                        ,_ic_base_dir=folderName,_rmfile='result')

            elif count>0:

                # Step 1.b.1 : ReBuild a new fingerprint dataset by former 'none'
                if count == 1:
                    get_iter_fp(txt_path=iterate_root_path+'/iter'+str(count-1)
                                , save_path=folderName
                                , formerFP_path=fpf_path)
                else:
                    get_iter_fp(txt_path=iterate_root_path + '/iter' + str(count - 1)
                                , save_path=folderName
                                , formerFP_path=iterate_root_path + '/iter' + str(count - 1))

                # Step 1.b.2 : Auto-Cluster
                fingerprintspilter.main(_sim=sim, _cmd='Cluster', _fingerPrintDir=folderName
                                        , _ic_base_dir=folderName,_rmfile='result')

            # Step 2 : Create 'none.txt' file for next iteration
            resultFilter.main(folderName)



if __name__ == 'main' or __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='cloth cluster by neural-fingerprints ',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--iter', help='Iterate count , default 0 means no iterate',
                        default=0, type=int)
    args = parser.parse_args()
    main(args.iter)


# fpdict =co .read_pk('/home/deepcam/Data/imagecluster/fingerprints.pk')
# name = dict(fpdict).keys()[0]
# s1 = fpdict[name]

