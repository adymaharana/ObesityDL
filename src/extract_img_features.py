import os, sys
import glob
#import cv2
from PIL import Image
from PIL import ImageOps
import csv
# sys.path.append('/home/ady/caffe/python')
import caffe
# import lmdb
import numpy as np
from caffe.proto import caffe_pb2

caffe.set_mode_cpu()

#Size of images
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224

modeldir = '../model'
modelname = 'VGG_CNN_F.caffemodel'
protofile = 'VGG_CNN_F_deploy_new.prototxt'
meanfile = 'VGG_mean.binaryproto'
imgdir = "../data/stb/stb_tracts_18/*png"
city = 'stb'

'''
Image processing helper function
'''

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    r,g,b = img.split()
    #Histogram Equalization
    # img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    # img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    # img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])
    rnew = ImageOps.equalize(r)
    gnew = ImageOps.equalize(g)
    bnew = ImageOps.equalize(b)

    #Image Resizing
    # img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)
    img = Image.merge("RGB", (rnew,gnew,bnew))
    img = img.resize((img_width, img_height), resample = Image.BICUBIC)

    return img

def vis_square(data):
    data = (data - data.min()) / (data.max() - data.min())
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = (((0, n ** 2 - data.shape[0]),
               (0, 1), (0, 1))
               + ((0, 0),) * (data.ndim - 3))
    data = np.pad(data, padding, mode = 'constant', constant_values = 1)

    data = data.reshape((n, n) + data.shape[1:]).transpose((0,2,1,3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    return(data)

'''
Reading mean image, caffe model and its weights
'''
#Read mean image
mean_blob = caffe_pb2.BlobProto()
#with open('/data/crime/mean.binaryproto') as f:
with open(os.path.join(modeldir, meanfile), 'rb') as f:
    mean_blob.ParseFromString(f.read())
mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
    (mean_blob.channels, mean_blob.height, mean_blob.width))


#Read model architecture and trained model's weights
#net = caffe.Net('/home/ubuntu/src/crime_deploy.prototxt',
#                '/home/ubuntu/crime_iter_10000.caffemodel',
#                caffe.TEST)

net = caffe.Net(os.path.join(modeldir, protofile), os.path.join(modeldir, modelname), caffe.TEST)

#Define image transformers
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', mean_array)
transformer.set_transpose('data', (2,0,1))

'''
Making predicitions
'''

test_img_paths = [img_path for img_path in glob.glob(imgdir)]
test_img_paths.sort()

print("Extracting Features")

#Extracting features
raw_features = []
finalimgs = []
count = 0
split = 0
outdir = '../out'
for img_path in test_img_paths:

    img = Image.open(img_path).convert('RGB')
    count += 1
    img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
    img = np.array(img)
    net.blobs['data'].data[...] = transformer.preprocess('data', img)
    net.forward()

    #for layer_name, blob in net.blobs.iteritems():
    #    print layer_name + '\t' + str(blob.data.shape)
    #for layer_name, param in net.params.iteritems():
    #    print layer_name + '\t' + str(param[0].data.shape), str(param[1].data.shape)

    raw_features.append(net.blobs['fc7'].data.tolist())
    finalimgs.append(img_path.split()[-1])
    print(count,)

    if count == 6000:
        raw_features = np.vstack(raw_features)
        np.save(os.path.join(outdir, city, 'features_tracts_fc7_z18_vgg_' + str(split) + '.npy'), raw_features)
        np.save(os.path.join(outdir, city, 'filenames_tracts_fc7_z18_vgg_' + str(split) + '.npy'), finalimgs)
        split += 1
        count = 0
        raw_features = []
        finalimgs = []

raw_features = np.vstack(raw_features)
np.save(os.path.join(outdir, city, 'features_tracts_fc7_z18_vgg_' + str(split) + '.npy'), raw_features)
np.save(os.path.join(outdir, city, 'filenames_tracts_fc7_z18_vgg_' + str(split) + '.npy'), finalimgs)
