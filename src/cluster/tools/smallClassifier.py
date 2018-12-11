import keras
from keras.preprocessing import image
import numpy as np
import pandas as pd
import os
import sys


imgs_folder_path = '/home/jc/Data/tianchi/TaoBaoClothesMatchingData/images/'
dim_items_data_path = '/home/jc/Data/tianchi/TaoBaoClothesMatchingData/tables/dim_items(new).txt'
top = 2

def get_model():
    """
    get a VGG16 or xception model from keras
    :return:
    """


    model = keras.applications.inception_v3.InceptionV3\
            (include_top=True,weights='imagenet',input_tensor=None,
             input_shape=(299,299,3),pooling=None
             ,classes=1000)

    return model

def get_label(img_path,model):

    img_size = 299

    img= image.load_img(img_path,target_size=(img_size,img_size))
    x = image.img_to_array(img)
    x = np.expand_dims(x,axis=0)
    x = keras.applications.inception_v3.preprocess_input(x)
    preds = model.predict(x)
    predictedLabel = keras.applications.inception_v3.decode_predictions(preds, top=top)[0]
    for i in range(predictedLabel.__len__()):
        predictedLabel[i] = str(predictedLabel[i][1]).split("\'")[0]

    return  predictedLabel

def get_most_predictLabel(p_lists):
    """"
    Get common predicted element or a 'None'
    """
    print (p_lists)
    preds_count = {}

    for p_list in p_lists:
        for val in p_list:
            if preds_count.has_key(val):
                preds_count[val] += 1
            else:
                preds_count[val] = 1

    print (preds_count)
    max_value = -1
    max_key = ''

    #print (preds_count)

    for key,value in preds_count.items():
        if value > max_value:
            max_value = value
            max_key = key

    return max_key




def main(imgs_path = ''):
    img_names = []
    model = get_model()
    for dirpath, dirnames, filenames in os.walk(imgs_path):
        img_names = filenames
        break

    preds = []

    for img in img_names:
        if img.find('jpg') > 0:
            preds.append(get_label(imgs_path + '/' + img , model ) )
    os.system('nautilus '+imgs_path)
    key = get_most_predictLabel(preds)
    f = open(imgs_path + '/' + key, 'a')
    f.write('')
    f.close()
    a = input()

main('/home/deepcam/IRoot/iter0/part0/cluster/cluster_with_16/cluster_0')