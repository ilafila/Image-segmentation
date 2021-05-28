import math
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Dinic import Graph
from PIL import Image
from image2graph import image2graph
import os


def generate_rect(corner, h, w):
    rect = []
    for i in range(h):
        for j in range(w):
            rect.append((corner[0]+i, corner[1]+j))
    return rect


def generate_interval(a, b, fat=1):
    x0, y0 = a[0], a[1]
    x1, y1 = b[0], b[1]
    interval = []
    deltax = abs(x1 - x0)
    deltay = abs(y1 - y0)
    error = 0
    deltaerr = (deltay + 1)
    y = y0
    diry = y1 - y0
    if diry > 0:
        diry = 1
    if diry < 0:
        diry = -1
    for x in range(x0, x1+1):
        for j in range(fat):
            interval.append((x, y+j))
        error = error + deltaerr
        if error >= (deltax + 1):
            y = y + diry
            error = error - (deltax + 1)
    return interval


def generate_scribbles_0_3():
    obj = generate_interval((130, 50), (165, 200), 5)
    obj += generate_rect((110, 260), 30, 4)
    bkg = generate_rect((50, 10), 3, 115)
    return obj, bkg


def generate_scribbles_4_4():
    obj = generate_interval((130, 50), (165, 200), 5)
    obj += generate_rect((110, 260), 30, 4)
    bkg = generate_rect((50, 10), 3, 115)
    return obj, bkg


def make_pixels(index, image_url):
    img = mpimg.imread('../images-320/' + image_url)
    img_shape = img.shape
    obj_scribble, bkg_scribble = [], []
    if 0 <= index <= 3:
        obj_scribble, bkg_scribble = generate_scribbles_0_3()
    elif index:
        obj_scribble, bkg_scribble = generate_scribbles_4_4()
    else:
        obj_scribble, bkg_scribble = generate_scribbles_4_4()
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
