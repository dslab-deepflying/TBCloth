import os,sys
import shutil
import re
import argparse

from keras import backend as K
K.clear_session()
import pandas as pd

#from src.cluster.imagecluster import main  # use pycharm run
from imagecluster import main as cluster # use python command line
from imagecluster import fingerprintspilter

iterCount = 0
sim = 0.55

# iterate_root_path = '/home/jc/IRoot'
iterate_root_path = '/home/deepcam/IRoot'

fp_path = '/home/deepcam/Data/imagecluster'

imagedir = '/home/deepcam/Data/tbcloth/imgs'


def get_iter_fp(txt_path,save_path):
    files = pd.read_csv(txt_path)



if __name__ == 'main' or __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='cloth cluster by neural-fingerprints ',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--iter', help='Iterate count , default 0 means no iterate',
                        default=0, type=int)
    args = parser.parse_args()

    iterCount = args.iter

    if iterCount == 0:
        cluster.main(imagedir=imagedir,ic_base_dir=fp_path)
    elif iterCount > 0:
        # If we have no fp exists , then get one
        if not os.path.exists(fp_path+'/fingerprints.pk'):
            cluster.get_fp(imagedir=imagedir,ic_base_dir=fp_path)

        # Delete former results by iterating
        for dirpath, dirnames, filenames in os.walk(iterate_root_path):
            for dirname in dirnames:
                if re.match('iter\d+',dirname) != None:
                    shutil.rmtree(iterate_root_path+'/'+dirname)
            break

        for count in range(iterCount):
            folderName = iterate_root_path+'/iter'+str(count)
            os.makedirs(folderName)

            if count == 0:
                fingerprintspilter.main(_sim=sim,_cmd='Cluster',_fingerPrintDir=fp_path
                                        ,_ic_base_dir=folderName)
            elif count>0:
                get_iter_fp(iterate_root_path+'/iter'+str(count-1), folderName)


