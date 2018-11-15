import os,sys
from src.cluster.imagecluster import main  # use pycharm run
from src.cluster.imagecluster import common as co
#from imagecluster import main   # use python command line
from keras import backend as K
K.clear_session()

import shutil
import random
import pandas as pd
from PIL import Image


sample_num = 200
sim = 0.5


tar_img_path = '/home/jc/codes/Projects/TBCloth/src/cluster/imgs/'  # for random sample
src_img_path = '/home/jc/Data/tianchi/TaoBaoClothesMatchingData/images/'
itemstxt_path = '/home/jc/codes/Projects/TBCloth/src/classifier/tools/items.txt'
ic_base_dir='imagecluster'

def random_sample():
    l1=list(pd.read_table(itemstxt_path,sep=' ')['itemid'])
    sp_l = random.sample(l1,sample_num)
    print(sp_l.__len__())

    for itemid in sp_l:
        try:
            shutil.copy(src_img_path + str(itemid) + '.jpg', tar_img_path)
        except Exception, e:
            # except FileNotFoundError : # python3
            print(str(itemid)+'.jpg lost !')
        continue


def gray_sacale():
    """
    trans the tar_img_path's image from rgb to gray_scale
    :return:
    """
    for roots, directs, files in os.walk(tar_img_path):
        break
    for file in files:
        I = Image.open(tar_img_path+file)
        L = I.convert('L')
        os.remove(tar_img_path + file)
        L.save(tar_img_path+file)


def remove_result(remove_src = True):
    """
    remove result of main generate
    :return:
    """
    if remove_src :
        for roots, directs, files in os.walk(tar_img_path):
            break
        for file in files:
            os.remove(tar_img_path + file)
    if os.path.exists(tar_img_path+'imagecluster'):
        shutil.rmtree(tar_img_path+'imagecluster')

def generate():
    #remove_result()
    #random_sample()
    #gray_sacale()
    main.main(tar_img_path, sim=sim,ic_base_dir=ic_base_dir)
    K.clear_session()

def readFP():
    a = co.read_pk(sys.path[0]+'/imgs/imagecluster/fingerprints.pk')
    print(a)


#remove_result()
remove_result(False)
#gray_sacale()
#random_sample()
generate()

#readFP()

