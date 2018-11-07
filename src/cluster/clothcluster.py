import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.cluster.imagecluster import main
from keras import backend as K
K.clear_session()

import shutil
import random
import pandas as pd
from PIL import Image


sample_num = 5
sim = 0.52

tar_img_path = '/home/jc/codes/Projects/imagecluster/imgs/'
src_img_path = '/home/jc/Data/tianchi/TaoBaoClothesMatchingData/images/'



def random_sample():
    l1=list(pd.read_table('items.txt',sep=' ')['itemid'])
    sp_l = random.sample(l1,sample_num)
    try:
        for itemid in sp_l:
            shutil.copy(src_img_path+str(itemid)+'.jpg',tar_img_path)
    except FileNotFoundError:
        print('emm...')


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
    shutil.rmtree(tar_img_path+'imagecluster')

def generate():
    #random_sample()
    #gray_sacale()
    main.main(tar_img_path, sim=sim)
    K.clear_session()


#gray_sacale()
#remove_result()
#remove_result(False)
#random_sample()
generate()

