#! /usr/bin/python
# -*- coding = utf-8 -*-

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import decode_predictions
import pandas as pd
import numpy as np
from keras.preprocessing import image





cate_txt_path = '/home/jc/codes/Projects/TBCloth/src/classifier/tools/cates.txt'
test_img_path = '/home/jc/codes/Projects/TBCloth/src/cluster/imgs/3007781.jpg'

def get_model():
    model = VGG16 \
        (include_top=True, weights='imagenet', input_tensor=None,
         input_shape=(224, 224, 3), pooling=None,
         classes=1000)
    return model

def main():
    cates = pd.read_table(cate_txt_path,sep=',')['cate']
    model = get_model()
    img = image.load_img(test_img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    pred = model.predict(x)
    print(list(pred[0])[770])
    print(decode_predictions(pred)[0])


main()
