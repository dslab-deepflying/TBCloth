from scipy.spatial import distance
from scipy.cluster import hierarchy
import numpy as np
import PIL.Image, os, shutil,sys
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input
from keras.models import Model

import tensorflow as tf
from tensorflow.python.framework import graph_util


import pandas as pd
import common as co
#from imagecluster import common as co

cate_index_txt_path = '/home/jc/codes/Projects/TBCloth/src/cluster/tools/catesIndex.txt'

pj = os.path.join


def get_model():
    """Keras Model of the VGG16 network, with the output layer set to the
    second-to-last fully connected layer 'fc2' of shape (4096,)."""
    # base_model.summary():
    #     ....
    #     block5_conv4 (Conv2D)        (None, 15, 15, 512)       2359808
    #     _________________________________________________________________
    #     block5_pool (MaxPooling2D)   (None, 7, 7, 512)         0
    #     _________________________________________________________________
    #     flatten (Flatten)            (None, 25088)             0
    #     _________________________________________________________________
    #     fc1 (Dense)                  (None, 4096)              102764544
    #     _________________________________________________________________
    #     fc2 (Dense)                  (None, 4096)              16781312
    #     _________________________________________________________________
    #     predictions (Dense)          (None, 1000)              4097000
    #
    base_model = InceptionV3(weights='imagenet', include_top=True)
    model = Model(inputs=base_model.input,
                 outputs=base_model.get_layer('avg_pool').output)
    #xception avg_pool
    #inceptionv3 avg_pool
    return model

def get_model2():

    output_graph_path = '/home/deepcam/Data/retrained_graph.pb'

    with tf.Session() as sess :
        tf.global_variables_initializer().run()
        output_graph_def = tf.GraphDef()
        with open( output_graph_path , 'rb' ) as f :
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def,name='')

        summary_writer = tf.summary.FileWriter('log',sess.graph)




def fingerprint(fn, model, size):
    """Load image from file `fn`, resize to `size` and run through `model`
    (keras.models.Model).

    Parameters
    ----------
    fn : str
        filename
    model : keras.models.Model instance
    size : tuple
        input image size (width, height), must match `model`, e.g. (224,224)

    Returns
    -------
    fingerprint : 1d array
    """
    #print(fn)
    
    # keras.preprocessing.image.load_img() uses img.rezize(shape) with the
    # default interpolation of PIL.Image.resize() which is pretty bad (see
    # imagecluster/play/pil_resample_methods.py). Given that we are restricted
    # to small inputs of 224x224 by the VGG network, we should do our best to
    # keep as much information from the original image as possible. This is a
    # gut feeling, untested. But given that model.predict() is 10x slower than
    # PIL image loading and resizing .. who cares.
    #
    # (224, 224, 3)
    ##img = image.load_img(fn, target_size=size)
    img = PIL.Image.open(fn).resize(size, 3)
    
    # (224, 224, {3,1})
    arr3d = image.img_to_array(img)
    
    # (224, 224, 1) -> (224, 224, 3)
    #
    # Simple hack to convert a grayscale image to fake RGB by replication of
    # the image data to all 3 channels.
    #
    # Deep learning models may have learned color-specific filters, but the
    # assumption is that structural image features (edges etc) contibute more to
    # the image representation than color, such that this hack makes it possible
    # to process gray-scale images with nets trained on color images (like
    # VGG16).
    if arr3d.shape[2] == 1:
        arr3d = arr3d.repeat(3, axis=2)

    # Indeed, this gray-scale-hack code does not work at all
    # You will find they have no difference between source-image
    # when you display them after that
    # PIL.Image._show(image.array_to_img(arr3d))
    # I = Image.open(tar_img_path+file) # PIL.Image
    # L = I.convert('L')

    # (1, 224, 224, 3)
    arr4d = np.expand_dims(arr3d, axis=0)
    
    # (1, 224, 224, 3)
    arr4d_pp = preprocess_input(arr4d)

    # Original code of return all of this array
    return model.predict(arr4d_pp)[0, :]

    # use prediction of cloth to be a fingerprint
    # however it has poor ability to cluster them ...

    # cates = pd.read_table(cate_index_txt_path,sep=',')['index']
    # arr_p = model.predict(arr4d_pp)[0,:]
    # arr_p = [arr_p[i] for i in cates]
    #
    # return arr_p



# Cannot use multiprocessing (only tensorflow backend tested):
# TypeError: can't pickle _thread.lock objects
# The error doesn't come from functools.partial since those objects are
# pickable since python3. The reason is the keras.model.Model, which is not
# pickable. However keras with tensorflow backend runs multi-threaded
# (model.predict()), so we don't need that. I guess it will scale better if we
# parallelize over images than to run a muti-threaded tensorflow on each image,
# but OK. On low core counts (2-4), it won't matter.
#
##def _worker(fn, model, size):
##    print(fn)
##    return fn, fingerprint(fn, model, size)
##
##def fingerprints(files, model, size=(224,224)):
##    worker = functools.partial(_worker,
##                               model=model,
##                               size=size)
##    pool = multiprocessing.Pool(multiprocessing.cpu_count())
##    return dict(pool.map(worker, files))


def fingerprints(files, model, size=(224,224)):
    """Calculate fingerprints for all `files`.

    Parameters
    ----------
    files : sequence
        image filenames
    model, size : see :func:`fingerprint`

    Returns
    -------
    fingerprints : dict
        {filename1: array([...]),
         filename2: array([...]),
         ...
         }
    """
    result = {}
    num=files.__len__()
    i=0
    print('Creating fingerprints')
    for fn in files:
        i+=1
        result[fn]=fingerprint(fn,model,size)
        sys.stdout.write('\r[%.2f%%]' % (i*100.0/num))
        sys.stdout.flush()
    # return dict((fn, fingerprint(fn, model, size)) for fn in files)
    print('\n')
    return result

def cluster(fps, sim=0.5, method='average', metric='cosine'):
    # metric euclidean
    """Hierarchical clustering of images based on image fingerprints.

    Parameters
    ----------
    fps: dict
        output of :func:`fingerprints`
    sim : float 0..1
        similarity index
    method : see scipy.hierarchy.linkage(), all except 'centroid' produce
        pretty much the same result
    metric : see scipy.hierarchy.linkage(), make sure to use 'euclidean' in
        case of method='centroid', 'median' or 'ward'

    Returns
    -------
    clusters : nested list
        [[filename1, filename5],                    # cluster 1
         [filename23],                              # cluster 2
         [filename48, filename2, filename42, ...],  # cluster 3
         ...
         ]
    """
    assert 0 <= sim <= 1, "sim not 0..1"
    # array(list(...)): 2d array
    #   [[... fingerprint of image1 (4096,) ...],
    #    [... fingerprint of image2 (4096,) ...],
    #    ...
    #    ]
    dfps = distance.pdist(np.array(list(fps.values())), metric)
    files = list(fps.keys())
    # hierarchical/agglomerative clustering (Z = linkage matrix, construct
    # dendrogram)
    Z = hierarchy.linkage(dfps, method=method, metric=metric)
    # cut dendrogram, extract clusters
    cut = hierarchy.fcluster(Z, t=dfps.max()*(1.0-sim), criterion='distance')
    cluster_dct = dict((ii,[]) for ii in np.unique(cut))
    for iimg,iclus in enumerate(cut):
        cluster_dct[iclus].append(files[iimg])

    return list(cluster_dct.values())


def make_links(clusters, cluster_dr):
    # group all clusters (cluster = list_of_files) of equal size together
    # {number_of_files1: [[list_of_files], [list_of_files],...],
    #  number_of_files2: [[list_of_files],...],
    # }
    cdct_multi = {}
    cdct_none = []

    i=1

    for x in clusters:
        sys.stdout.write('\rdealing: [' + str(int(i * 100.0 / clusters.__len__())) + '%]')
        i += 1

        nn = len(x)
        if nn > 1:
            if not (nn in cdct_multi.keys()):
                cdct_multi[nn] = [x]
            else:
                cdct_multi[nn].append(x)
        else:
            cdct_none.append(x)

    count = 0
    print("\ncluster dir: {}".format(cluster_dr))
    if os.path.exists(cluster_dr):
        shutil.rmtree(cluster_dr)
    for nn in np.sort(list(cdct_multi.keys())):
        cluster_list = cdct_multi[nn]
        count += nn*len(cluster_list)
        print("{} : {}".format(nn, len(cluster_list)))
        for iclus, lst in enumerate(cluster_list):
            dr = pj(cluster_dr,
                    'cluster_with_{}'.format(nn),
                    'cluster_{}'.format(iclus))
            for fn in lst:
                link = pj(dr, os.path.basename(fn))
                if not os.path.exists(os.path.dirname(link)):
                    #shutil.rmtree(os.path.dirname(link))
                    os.makedirs(os.path.dirname(link))
                os.symlink(os.path.abspath(fn), link)

    count += cdct_none.__len__()
    print ('none cluster : %d [%.2f]' % (cdct_none.__len__(),cdct_none.__len__()*1.0/count))
    for iclus, lst in enumerate(cdct_none):
        dr = pj(cluster_dr,'none')
        for fn in lst:
            link = pj(dr, os.path.basename(fn))
            if not os.path.exists(os.path.dirname(link)):
                # shutil.rmtree(os.path.dirname(link))
                os.makedirs(os.path.dirname(link))
            os.symlink(os.path.abspath(fn), link)

get_model2()