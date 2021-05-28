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


def make_pixels(index, image_url, lambda_const, sigma_const):
    img = mpimg.imread('../images-320/' + image_url)
    img_shape = img.shape
    obj_scribble, bkg_scribble = scribbles[index]()
    underlying_graph = image2graph(img, obj_scribble, bkg_scribble, lambda_const, sigma_const)
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
    array_of_lambdas = [1, 30, 100]
    array_of_sigmas = [1, 40, 100]
    directory = '../images-320'
    images = os.listdir(directory)
    images.sort()
    results_of_correct_pixles = []
    results_of_jacard_metrics = []
    for idx, image_url in enumerate(images):
        for lambda_const in array_of_lambdas:
            for sigma_const in array_of_sigmas:
                make_pixels(idx, image_url, lambda_const, sigma_const)
                true_segments = mpimg.imread('../image-segments-320/' + image_url.split('-')[0] + '-320.jpg')
                predicted_segments = mpimg.imread('../images-segments-prediction-320/' + image_url)
                true_segments = true_segments[:, :, :1].flatten().reshape(predicted_segments.shape)
                correct_pixels, Jaccard = analyze(true_segments, predicted_segments)
                # TODO write in file too
                print('Правильно угаданных пикселей: ', correct_pixels)
                print('Мера Жаккара: ', Jaccard)
                print('--------------------------------------------------------')

def analyze_lambda():
    array_of_lambdas = [1, 30, 100]
    directory = '../images-320'
    images = os.listdir(directory)
    images.sort()
    results_of_correct_pixles = []
    results_of_jacard_metrics = []
    for lambda_const in array_of_lambdas:
        for idx, image_url in enumerate(images):
            make_pixels(idx, image_url, lambda_const, 40)
            true_segments = mpimg.imread('../image-segments-320/' + image_url.split('-')[0] + '-320.jpg')
            predicted_segments = mpimg.imread('../images-segments-prediction-320/' + image_url)
            true_segments = true_segments[:, :, :1].flatten().reshape(predicted_segments.shape)
            correct_pixels, Jaccard = analyze(true_segments, predicted_segments)
            # TODO write in file too
            print('Правильно угаданных пикселей: ', correct_pixels)
            print('Мера Жаккара: ', Jaccard)
            print('--------------------------------------------------------')
        file = open('../segmentation-tests/analyzeLambda.txt', 'w')
        file.write('--------------------------------------------------------')
        file.write('Значение лямбда: ' + str(lambda_const), '\n')
        file.write('Минимальное значение правильно угаданных пикселей: ' + str(min(results_of_correct_pixles)), '\n')
        file.write('Максимальное значение правильно угаданных пикселей: ' + str(max(results_of_correct_pixles)), '\n')
        file.write('Среднее значение правильно угаданных пикселей: ' + str(
            sum((int(results_of_correct_pixles[i]) for i in range(0, int(len(results_of_correct_pixles))))) / len(
                results_of_correct_pixles)), '\n')
        file.write('Минимальное значение меры Жаккара: ' + str(min(results_of_jacard_metrics)), '\n')
        file.write('Максимальное значение меры Жаккара: ' + str(max(results_of_jacard_metrics)), '\n')
        file.write('Среднее значение меры Жаккара: ' + str(
            sum((int(results_of_jacard_metrics[i]) for i in range(0, int(len(results_of_jacard_metrics))))) / len(
                results_of_jacard_metrics)), '\n')

def analyze_sigma():
    array_of_sigmas = [1, 40, 100]
    directory = '../images-320'
    images = os.listdir(directory)
    images.sort()
    for sigma_const in array_of_sigmas:
        results_of_correct_pixles = []
        results_of_jacard_metrics = []
        for idx, image_url in enumerate(images):
            make_pixels(idx, image_url, 30, sigma_const)
            true_segments = mpimg.imread('../image-segments-320/' + image_url.split('-')[0] + '-320.jpg')
            predicted_segments = mpimg.imread('../images-segments-prediction-320/' + image_url)
            true_segments = true_segments[:, :, :1].flatten().reshape(predicted_segments.shape)
            correct_pixels, Jaccard = analyze(true_segments, predicted_segments)
            # TODO write in file too
            print('Правильно угаданных пикселей: ', correct_pixels)
            results_of_correct_pixles.append(correct_pixels)
            print('Мера Жаккара: ', Jaccard)
            results_of_jacard_metrics.append(Jaccard)
            print('--------------------------------------------------------')
        file = open('../segmentation-tests/analyzeSigma.txt', 'w')
        file.write('--------------------------------------------------------')
        file.write('Значение сигма: '+str(sigma_const), '\n')
        file.write('Минимальное значение правильно угаданных пикселей: ' + str(min(results_of_correct_pixles)), '\n')
        file.write('Максимальное значение правильно угаданных пикселей: ' + str(max(results_of_correct_pixles)), '\n')
        file.write('Среднее значение правильно угаданных пикселей: ' + str(sum((int(results_of_correct_pixles[i]) for i in range(0, int(len(results_of_correct_pixles)))))/len(results_of_correct_pixles)), '\n')
        file.write('Минимальное значение меры Жаккара: ' + str(min(results_of_jacard_metrics)), '\n')
        file.write('Максимальное значение меры Жаккара: ' + str(max(results_of_jacard_metrics)), '\n')
        file.write('Среднее значение меры Жаккара: ' + str(
            sum((int(results_of_jacard_metrics[i]) for i in range(0, int(len(results_of_jacard_metrics))))) / len(
                results_of_jacard_metrics)), '\n')


analyze_lambda()
analyze_sigma()

