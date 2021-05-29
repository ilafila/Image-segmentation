import math
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Dinic import Graph
from PIL import Image
from image2graph import image2graph
from scribbles import generate_rect, scribbles
import os


def make_pixels(index, image_url, **kvargs):
    img = mpimg.imread('../images-320/' + image_url)
    img_shape = img.shape
    obj_scribble, bkg_scribble = scribbles[index]()
    image_graph = image2graph(img, obj_scribble, bkg_scribble, **kvargs)
    start = time.time()
    one_item = image_graph.min_cut()
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
        print(image_url)
        make_pixels(idx, image_url)
        true_segments = mpimg.imread('../image-segments-320/' + image_url.split('-')[0] + '-320.jpg')
        predicted_segments = mpimg.imread('../images-segments-prediction-320/' + image_url)
        true_segments = true_segments[:, :, :1].flatten().reshape(predicted_segments.shape)
        correct_pixels, Jaccard = analyze(true_segments, predicted_segments)
        print('Правильно угаданных пикселей: ', correct_pixels)
        print('Мера Жаккара: ', Jaccard)
        print('--------------------------------------------------------')


def analyze_lambda_and_sigma(lambdas, sigmas):
    directory = '../images-320'
    images = os.listdir(directory)
    images.sort()
    results_of_correct_pixles = []
    results_of_jacard_metrics = []
    for lambda_const in lambdas:
        for sigma_const in sigmas:
            for idx, image_url in enumerate(images):
                make_pixels(idx, image_url, lambda_const, sigma_const)
                true_segments = mpimg.imread('../image-segments-320/' + image_url.split('-')[0] + '-320.jpg')
                predicted_segments = mpimg.imread('../images-segments-prediction-320/' + image_url)
                true_segments = true_segments[:, :, :1].flatten().reshape(predicted_segments.shape)
                correct_pixels, Jaccard = analyze(true_segments, predicted_segments)
                print('Правильно угаданных пикселей: ', correct_pixels)
                results_of_correct_pixles.append(correct_pixels)
                print('Мера Жаккара: ', Jaccard)
                results_of_jacard_metrics.append(Jaccard)
                print('--------------------------------------------------------')
            file = open('analyzeLambdaSigma'+str(lambda_const)+'.txt', 'w')
            file.write('Значение лямбда: ' + str(lambda_const)+' \n')
            file.write('Значение сигма: ' + str(sigma_const) + ' \n')
            file.write('Минимальное значение правильно угаданных пикселей: '+str(min(results_of_correct_pixles))+' \n')
            file.write('Максимальное значение правильно угаданных пикселей: '+str(max(results_of_correct_pixles))+' \n')
            sum_pixels = 0
            for i in results_of_correct_pixles:
                sum_pixels += i
            file.write('Среднее значение правильно угаданных пикселей: '+str(sum_pixels/len(results_of_correct_pixles))+' \n')

            file.write('Минимальное значение меры Жаккара: '+str(min(results_of_jacard_metrics))+' \n')
            file.write('Максимальное значение меры Жаккара: '+str(max(results_of_jacard_metrics))+' \n')
            sum_jacard = 0
            for j in results_of_jacard_metrics:
                sum_jacard += j
            file.write('Среднее значение меры Жаккара: '+str(sum_jacard/len(results_of_jacard_metrics)))
            file.close()


def interactive_segmentation(image_url):
    img = mpimg.imread('../interactive-images/' + image_url)
    img_shape = img.shape
    print('Введите прямоугольник, относящийся к объекту')
    obj_x0, obj_y0, obj_h, obj_w = list(map(int, input().split()))
    print('Введите прямоугольник, относящийся к фону')
    bkg_x0, bkg_y0, bkg_h, bkg_w = list(map(int, input().split()))
    obj_scribble, bkg_scribble = generate_rect((obj_x0, obj_y0), obj_h, obj_w), \
                                 generate_rect((bkg_x0, bkg_y0), bkg_h, bkg_w),
    image_graph = image2graph(img, obj_scribble, bkg_scribble)
    to_obj = image_graph.min_cut()
    bin_img = Image.new(mode='1', size=(img_shape[1], img_shape[0]), color=0)
    for i, val in enumerate(to_obj):
        if val:
            bin_img.putpixel((i % img_shape[1], i // img_shape[1]), 1)
    bin_img.save('../interactive-images-segments-prediction-320/' + image_url, 'JPEG')
    cont = True
    while cont:
        print("Введите дополнительный пиксели в формате: 'obj/bkg/stop x0 y0 h w'")
        inp = input()
        command = inp.split()[0]
        if command == 'stop':
            cont = False
            break
        else:
            x0, y0, h, w = list(map(int, inp.split()[1:]))
            pixels = generate_rect((x0, y0), h, w)
            for pixel in pixels:
                if command == 'obj':
                    image_graph.change_to_obj(pixel)
                elif command == 'bkg':
                    image_graph.change_to_bkg(pixel)
        one_item = image_graph.min_cut()
        bin_img = Image.new(mode='1', size=(img_shape[1], img_shape[0]), color=0)
        for i, val in enumerate(one_item):
            if val:
                bin_img.putpixel((i % img_shape[1], i // img_shape[1]), 1)
        bin_img.save('../interactive-images-segments-prediction-320/' + image_url, 'JPEG')


# interactive_segmentation('banana1-gr-320.jpg')
# analyze_lambda_and_sigma([1, 30, 100], [1, 40, 100])
# analyze_all()
# solo_test(11)
