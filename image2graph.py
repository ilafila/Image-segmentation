import math
import numpy as np
from scipy.special import erf
from Dinic import Graph


def laplace(x):
    return erf(x/2**0.5)/2

# constants
# TODO need to analyze for best params
K = 2
bins = 20
step = math.ceil(256 / bins)
lambda_const = 50
sigma_const = 10
epsilon = 1e-7


def generate_probs(img, interest):
    # определяем вероятности попадения в блоки гистограммы
    hist = [0] * bins
    mu = 0
    for (x, y) in interest:
        mu += img[x][y]
    mu /= len(interest)
    sigma = 0
    for (x, y) in interest:
        sigma += (img[x][y] - mu)**2
    sigma = math.sqrt(sigma / (len(interest)-1))
    for i in range(bins):
        b = (step*(i+1) - mu) / sigma
        a = (step*i - mu) / sigma
        hist[i] = laplace(b) - laplace(a)
    return hist


def image2graph(img, obj, bkg):
    number_of_nodes = len(img.ravel())
    number_of_rows = len(img)
    number_of_cols = len(img[0])
    obj_probs = generate_probs(img, obj)
    bkg_probs = generate_probs(img, bkg)
    obj_set = set(obj)
    bkg_set = set(bkg)
    obj_terminal, bkg_terminal = number_of_nodes, number_of_nodes+1
    graph = Graph(n=number_of_nodes+2, source=number_of_nodes, target=number_of_nodes+1)
    for i in range(number_of_rows):
        for j in range(number_of_cols):
            if (i, j) in obj_set:
                graph.add_edge(obj_terminal, number_of_cols * i + j, K)
                graph.add_edge(number_of_cols * i + j, bkg_terminal, 0)
            elif (i, j) in bkg_set:
                graph.add_edge(obj_terminal, number_of_cols * i + j, 0)
                graph.add_edge(number_of_cols*i + j, bkg_terminal, K)
            else:
                condition_obj_prob = obj_probs[img[i][j] // step] \
                                     / (obj_probs[img[i][j] // step] + bkg_probs[img[i][j] // step])
                condition_bkg_prob = bkg_probs[img[i][j] // step] \
                                     / (obj_probs[img[i][j] // step] + bkg_probs[img[i][j] // step])
                R_obj = -np.log(min(condition_obj_prob + epsilon, 1))
                R_bkg = -np.log(min(condition_bkg_prob + epsilon, 1))
                graph.add_edge(obj_terminal, number_of_cols*i + j, lambda_const*R_bkg)
                graph.add_edge(number_of_cols*i + j, bkg_terminal, lambda_const*R_obj)
            intensity = img[i][j]
            if i > 0:
                other_intensity = img[i-1][j]
                weight = np.exp(-((int(intensity)-int(other_intensity))**2) / (2 * (sigma_const**2)))
                graph.add_edge(number_of_cols*i + j, number_of_cols*(i-1) + j, weight)
            if i < number_of_rows-1:
                other_intensity = img[i+1][j]
                weight = np.exp(-((int(intensity) - int(other_intensity)) ** 2) / (2 * (sigma_const ** 2)))
                graph.add_edge(number_of_cols * i + j, number_of_cols * (i+1) + j, weight)
            if j > 0:
                other_intensity = img[i][j-1]
                weight = np.exp(-((int(intensity) - int(other_intensity)) ** 2) / (2 * (sigma_const ** 2)))
                graph.add_edge(number_of_cols * i + j, number_of_cols*i + j - 1, weight)
            if j < number_of_cols-1:
                other_intensity = img[i][j+1]
                weight = np.exp(-((int(intensity) - int(other_intensity)) ** 2) / (2 * (sigma_const ** 2)))
                graph.add_edge(number_of_cols * i + j, number_of_cols*i + j + 1, weight)
    return graph
