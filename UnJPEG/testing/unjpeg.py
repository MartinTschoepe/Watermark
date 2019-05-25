import os
import sys
import timeit

import numpy
import scipy
import math
import imageio

import theano
import theano.tensor as T

from PIL import Image

import pickle

import sys
sys.path.append('../training/')

import matplotlib as mlp
from mlp import MLP, TopLayer, HiddenLayer, unjpeg, rgb2ycbcr, ycbcr2rgb

def apply_on_folder(directory):
    for filename in os.listdir(directory):
        filename = directory + "/" + filename
        if filename.endswith(".JPG") or filename.endswith(".jpg"):
            blocksize = numpy.uint32(numpy.sqrt(classifier.hiddenLayers[0].W.get_value().shape[0]/3))
            rgbim = imageio.imread(filename,pilmode='RGB')/255
            im = rgb2ycbcr(rgbim)

            cleanim = ycbcr2rgb(unjpeg(im,classifier,blocksize,0.58,0.38))

            res = Image.fromarray(numpy.uint8(numpy.round(cleanim*255)),mode='RGB')
            filename = filename.replace("jpg", "png")
            filename = filename.replace("JPG", "png")
            print(filename)
            res.save(filename)

if __name__ == '__main__':
    # load the saved model  
    if theano.config.device.startswith("gpu"):
        with open('gpu_model.pkl', 'rb') as f:
            classifier = pickle.load(f)
    else:
        with open('cpu_model.pkl', 'rb') as f:
            classifier = pickle.load(f)
        
    directory1 = "../../Random3"
    apply_on_folder(directory1)

