import math
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Dinic import Graph
from PIL import Image
from image2graph import image2graph
import os


def generate_banana1_scribbles():
    # эмитирует то, что мы отметили как фон и обьект
    obj = []
    for i in range(150, 185):
        obj.append((i, 50 + 2 * (i - 150)))
        obj.append((i, 50 + 2 * (i - 150) + 1))
        obj.append((i, 50 + 2 * (i - 150) + 2))
        obj.append((i, 50 + 2 * (i - 150) + 3))
        obj.append((i, 50 + 2 * (i - 150) + 4))
        obj.append((i, 50 + 2 * (i - 150) + 5))
    for i in range(110, 150):
        obj.append((i, 260))
        obj.append((i, 261))
        obj.append((i, 262))

    bkg = []
    for j in range(10, 125):
        bkg.append((50, j))
        bkg.append((51, j))
        bkg.append((52, j))

    return obj, bkg


def make_pixels(image_url):
    img = mpimg.imread('../images-320/' + image_url)
    img_shape = img.shape
    # TODO switch: different scribbles for different images
    obj_scribble, bkg_scribble = generate_banana1_scribbles()

    underlying_graph = image2graph(img, obj_scribble, bkg_scribble)
    start = time.time()
    flow = underlying_graph.dinic()
    one_item = underlying_graph.min_cut()
    end = time.time()
    print(image_url)
    print('percent of object: ', sum(one_item)/(img_shape[1]*img_shape[0]) * 100)
    print("Time in seconds", "%.3f" % (end - start))
    print('Max flow: ', flow)

    bin_img = Image.new(mode='1', size=(img_shape[1], img_shape[0]), color=0)
    for i, val in enumerate(one_item):
        if val:
            bin_img.putpixel((i % img_shape[1], i // img_shape[1]), 1)
    bin_img.save('../images-segments-prediction-320/' + image_url, 'JPEG')


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
    for image_url in images:
        make_pixels(image_url)
        true_segments = mpimg.imread('../image-segments-320/'+image_url.split('-')[0]+'-320.jpg')
        predicted_segments = mpimg.imread('../images-segments-prediction-320/'+image_url)
        true_segments = true_segments[:, :, :1].flatten().reshape(predicted_segments.shape)
        correct_pixels, Jaccard = analyze(true_segments, predicted_segments)
        # TODO write in file too
        print('Правильно угаданных пикселей: ', correct_pixels)
        print('Мера Жаккара: ', Jaccard)
        print('--------------------------------------------------------')


analyze_all()
