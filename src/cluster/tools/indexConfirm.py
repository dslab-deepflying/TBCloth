#! /usr/bin/python
# -*- coding = utf-8 -*-

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import decode_predictions
import pandas as pd
import numpy as np
from keras.preprocessing import image


imgnet_txt_path = '/home/jc/codes/Projects/TBCloth/src/cluster/tools/imagenet1000_clsid_to_human.txt'
cate_txt_path = '/home/jc/codes/Projects/TBCloth/src/classifier/tools/cates.txt'
test_img_path = '/home/jc/codes/Projects/TBCloth/src/cluster/imgs/3007781.jpg'

def get_model():
    '''
    get a vgg16 model fot test
    :return:
    '''
    model = VGG16 \
        (include_top=True, weights='imagenet', input_tensor=None,
         input_shape=(224, 224, 3), pooling=None,
         classes=1000)
    return model

def main():
    """
    Get source categories' indices in image-net-prediction array
    we get some cloths here , you can get your own list for this
    :return:
    """
    srcCates = pd.read_table(cate_txt_path,sep=',')['cate']
    allCates = pd.read_table(imgnet_txt_path,sep=':')['content']
    dic = {}
    for item in srcCates:
        i=0
        for cot in allCates:
            i+=1
            if str(cot).find(item)>-1:
                if(dic.has_key(str(cot))):
                    print ('Opps dic dump')
                else:
                    dic[item] = i

    # You'd better add this row with no space manually:
    # name,index
    # for later cluster's work.(or pd.read_table() then add it)
    pd.Series(dic).sort_values().to_csv('catesIndex.txt')

def model_test():
    """
    If you never trust a guy who has no official note,
    you can have a try of this txt file
    (I tried 10 times , all works)
    :return:
    """
    cates = pd.read_table(cate_txt_path, sep=',')['cate']
    model = get_model()
    img = image.load_img(test_img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    pred = model.predict(x)

    # The 770 is the index of 'running_shoe' in that txt file
    # you will find they have the same number (Other also works)
    print(list(pred[0])[770])
    print(decode_predictions(pred)[0][0])


main()

