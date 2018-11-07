import keras
from keras.preprocessing import image
import numpy as np
import pandas as pd
import os
import sys


imgs_folder_path = '/home/jc/Data/tianchi/TaoBaoClothesMatchingData/images/'
dim_items_data_path = '/home/jc/Data/tianchi/TaoBaoClothesMatchingData/tables/dim_items(new).txt'
top = 5

def get_model(model_name = 'vgg16'):
    """
    get a VGG16 or xception model from keras
    :return:
    """

    if model_name == 'vgg16':
        model = keras.applications.vgg16.VGG16\
            (include_top=True,weights='imagenet',input_tensor=None,
            input_shape=(224,224,3),pooling=None,
            classes=1000)
    elif model_name=='xception':
        model = keras.applications.xception.Xception\
            (include_top=True,weights='imagenet',input_tensor=None,
             input_shape=(299,299,3),pooling=None
             ,classes=1000)
    elif model_name == 'resnet':
        model = keras.applications.resnet50.ResNet50 \
            (include_top=True, weights='imagenet', input_tensor=None,
             input_shape=(224, 224, 3), pooling=None
             , classes=1000)
    return model

def get_label(img_path,model,model_name = 'vgg16'):


    if model_name == 'vgg16':
        img_size = 224
    elif model_name =='xception':
        img_size = 299
    elif model_name == 'resnet':
        img_size = 224

    img= image.load_img(img_path,target_size=(img_size,img_size))
    x=image.img_to_array(img)
    x= np.expand_dims(x,axis=0)

    if model_name == 'vgg16':
        x= keras.applications.vgg16.preprocess_input(x)
        preds = model.predict(x)
        predictedLabel = keras.applications.vgg16.decode_predictions(preds, top=top)[0]


    elif model_name == 'xception':
        x = keras.applications.xception.preprocess_input(x)
        preds = model.predict(x)
        predictedLabel = keras.applications.xception.decode_predictions(preds, top=top)[0]

    elif model_name == 'resnet':
        x = keras.applications.resnet50.preprocess_input(x)
        preds = model.predict(x)
        predictedLabel = keras.applications.resnet50.decode_predictions(preds, top=top)[0]

    #predictedLabel = str(predictedLabel).split("\'")[0]

    #print('Predicted:', predictedLabel)


    # for pred in preds:
    #     print(pred[-1:])
    #     top_indices = pred.argsort()[-3:][::-1]
    #     print(top_indices)
    return  predictedLabel

def get_same_predictLabel(p_list_1,p_list_2):
    """"
    Get common predicted element or a 'None'
    """
    ref = list(pd.read_csv(sys.path[0]+'/cates.txt')['cate'])

    for i in range(top):
        p_list_1[i] = str(p_list_1[i][1]).split("\'")[0]
        p_list_2[i] = str(p_list_2[i][1]).split("\'")[0]

    r1 = [val for val in p_list_1 if(val in ref)]
    r2 = [val for val in p_list_2 if(val in ref)]
    if r1.__len__() + r2.__len__() == 0:
        return  'None'
    elif r1.__len__()==0 and r2.__len__()!=0:
        return r2[0]
    elif r1.__len__()!=0 and r2.__len__() == 0:
        return r1[0]
    else:
        l_comon = [val for val in r1 if (val in r2)]
        # l_comon.count()
        if (l_comon.__len__() > 0):
            return l_comon[0]
        else:
            return str(r1[0])+"/"+str(r2[0])



def main():
    modelVGG = get_model('vgg16')
    modelXcep = get_model('xception')
    modelResset = get_model('resnet')


    dim_items_data \
        = pd.read_table(dim_items_data_path,skiprows=0,header=None,sep=' ',names=['itemID','-','-','-'])
    item_ids = dim_items_data['itemID'][:5]

    labels = []
    label = ''

    amount = item_ids.__len__()
    former = -1
    precent = 0
    i=0

    for item in item_ids:
        img_path=imgs_folder_path+str(item)+".jpg"
        if os.path.exists(img_path):
            label1 = get_label(img_path=img_path,model=modelVGG,model_name='vgg16')
            label2 = get_label(img_path=img_path,model=modelXcep,model_name='xception')
            label = get_same_predictLabel(label1,label2)


        precent = int((i + 1.0) / amount * 100)
        if former!= precent:
            former = precent
            print('[-'+'\033[0;32;40m'+'='*(precent/2)+'>'+'\033[0m'+'.'*(50 - (precent/2))+'] [%'+'%3d]' % precent)
        i+=1
        labels.append(label)

    dataFrames = pd.DataFrame({'itmeid':item_ids,'label':labels})
    dataFrames.to_csv(sys.path[0]+"/items.txt",index=False,sep=' ')

    print(dataFrames)


main()
