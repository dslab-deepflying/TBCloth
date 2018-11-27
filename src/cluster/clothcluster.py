import os,sys
import shutil
import re
import argparse

from imagecluster import common as co
import pandas as pd

#from src.cluster.imagecluster import main  # use pycharm run
from imagecluster import main as cluster # use python command line
from imagecluster import fingerprintspilter
from tools import resultFilter


iterCount = 0
sim = 0.55

# iterate_root_path = '/home/jc/IRoot'
iterate_root_path = '/home/deepcam/IRoot'

fpf_path = '/home/deepcam/Data/imagecluster/'

imagedir = '/home/deepcam/Data/tbcloth/imgs'

def get_iter_fp(txt_path,save_path,formerFP_path):

    txt_path += '/none.txt'
    formerFP_path += 'fingerprints.pk'

    files = pd.read_csv(txt_path,header=None,index_col=None)
    files = list(files[0])
    print (files.__len__())
    fpdict = co.read_pk(formerFP_path)
    print (len(fpdict))
    newdict={}
    for fname in files:
        tkey = imagedir+'/'+fname
        newdict[tkey] = fpdict[tkey]
    co.write_pk(newdict, save_path+'/fingerprints.pk')

# get_iter_fp(txt_path='/home/deepcam/ictest/nones.txt'
#             , save_path='/home/deepcam/IRoot',
#             formerFP_path='/home/deepcam/Data/fp')


if __name__ == 'main' or __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='cloth cluster by neural-fingerprints ',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--iter', help='Iterate count , default 0 means no iterate',
                        default=0, type=int)
    args = parser.parse_args()
    iterCount = args.iter

    if iterCount == 0:
        print('No iterate , clustering ')
        cluster.main(imagedir=imagedir,ic_base_dir=fpf_path)
    elif iterCount > 0:

        print('Iterated clustering ')

        # If we have no fp exists , then get one
        if not os.path.exists(fpf_path+'/fingerprints.pk'):
            cluster.get_fp(imagedir=imagedir,ic_base_dir=fpf_path)

        # Delete former results by iterating
        for dirpath, dirnames, filenames in os.walk(iterate_root_path):
            for dirname in dirnames:
                if re.match('iter\d+',dirname) != None:
                    shutil.rmtree(iterate_root_path+'/'+dirname)
            break

        for count in range(iterCount):
            folderName = iterate_root_path+'/iter'+str(count)
            os.makedirs(folderName)

            print ('Iter %d \n' % count)

            if count == 0:

                # Step 1 : Auto-Cluster
                # If the mount of imgs is large , it will be automatically divided
                # into some smaller task to do
                fingerprintspilter.main(_sim=sim,_cmd='Cluster',_fingerPrintDir=fpf_path
                                        ,_ic_base_dir=folderName)
            elif count>0:

                # Step 1 : get 'none' imgs list
                # 'none' means no similar cluster or hard to tag them manually
                resultFilter.main(iterate_root_path+'/iter'+str(count-1))

                # Step 2 : ReBuild a new fingerprint dataset by former 'none'
                if count == 1:
                    get_iter_fp(txt_path=iterate_root_path+'/iter'+str(count-1)
                                , save_path=folderName
                                , formerFP_path=fpf_path)
                else:
                    get_iter_fp(txt_path=iterate_root_path + '/iter' + str(count - 1)
                                , save_path=folderName
                                , formerFP_path=iterate_root_path + '/iter' + str(count - 1))

                fingerprintspilter.main(_sim=sim, _cmd='Cluster', _fingerPrintDir=folderName
                                        , _ic_base_dir=folderName)

#cluster.get_fp(imagedir=imagedir,ic_base_dir='/home/deepcam/Data/fp')