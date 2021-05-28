import math
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Dinic import Graph
from PIL import Image
from image2graph import image2graph
from scribbles import scribbles
import os


def make_pixels(index, image_url):
    img = mpimg.imread('../images-320/' + image_url)
    img_shape = img.shape
    obj_scribble, bkg_scribble = scribbles[index]()
    underlying_graph = image2graph(img, obj_scribble, bkg_scribble)
    start = time.time()
    flow = underlying_graph.dinic()
    one_item = underlying_graph.min_cut()
    end = time.time()
    print('percent of object: ', sum(one_item)/(img_shape[1]*img_shape[0]) * 100)
    print("Time in seconds", "%.3f" % (end - start))
    bin_img = Image.new(mode='1', size=(img_shape[1], img_shape[0]), color=0)
    for i, val in enumerate(one_item):
        if val:
            bin_img.putpixel((i % img_shape[1], i // img_shape[1]), 1)
    bin_img.save('../images-segments-prediction-320/' + image_url, 'JPEG')


def solo_test(index):
    directory = '../images-320'
    images = os.listdir(directory)
    images.sort()
    image_url = images[index]
    make_pixels(index, image_url)
    true_segments = mpimg.imread('../image-segments-320/' + image_url.split('-')[0] + '-320.jpg')
    predicted_segments = mpimg.imread('../images-segments-prediction-320/' + image_url)
    true_segments = true_segments[:, :, :1].flatten().reshape(predicted_segments.shape)
    correct_pixels, Jaccard = analyze(true_segments, predicted_segments)
    print('Правильно угаданных пикселей: ', correct_pixels)
    print('Мера Жаккара: ', Jaccard)
    print('--------------------------------------------------------')


def analyze(true_segments, predicted_segments):
    correct = 0
    intercept = 0
    union = 0
    rows = len(true_segments)
    cols = len(true_segments[0])
    for i in range(rows):
        for j in range(cols):
            if abs(int(true_segments[i][j]) - int(predicted_segments[i][j])) < 10:
                correct += 1
            if true_segments[i][j] < 20 or predicted_segments[i][j] < 20:
                union += 1
            if true_segments[i][j] < 20 and predicted_segments[i][j] < 20:
                intercept += 1
    return correct / (rows*cols), intercept/union


def analyze_all():
    directory = '../images-320'
    images = os.listdir(directory)
    images.sort()
    for idx, image_url in enumerate(images):
        make_pixels(idx, image_url)
        true_segments = mpimg.imread('../image-segments-320/'+image_url.split('-')[0]+'-320.jpg')
        predicted_segments = mpimg.imread('../images-segments-prediction-320/'+image_url)
        true_segments = true_segments[:, :, :1].flatten().reshape(predicted_segments.shape)
        correct_pixels, Jaccard = analyze(true_segments, predicted_segments)
        # TODO write in file too
        print('Правильно угаданных пикселей: ', correct_pixels)
        print('Мера Жаккара: ', Jaccard)
        print('--------------------------------------------------------')


analyze_all()

