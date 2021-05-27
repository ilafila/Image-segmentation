import math
import numpy as np
from Dinic import Graph

# constants
K = 2
bins = 9
step = math.ceil(256 / bins)
lambda_const = 10
sigma_const = 5
epsilon = 1e-9


def generate_probs(img, interest):
    # определяем вероятности попадения в блоки гистограммы
    hist = [0] * bins
    for (x, y) in interest:
        hist[img[x][y] // step] += 1
    for i in range(bins):
        hist[i] /= len(interest)
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
                R_obj = -np.log(obj_probs[img[i][j] // step] + epsilon)
                R_bkg = -np.log(bkg_probs[img[i][j] // step] + epsilon)
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
