import math
import numpy as np
from scipy.special import erf
from Dinic import Graph


def laplace(x):
    return erf(x/2**0.5)/2


# constants
# TODO need to analyze for best params
bins = 10
step = math.ceil(256 / bins)
epsilon = 1e-4
K = 20000000


def generate_probs(img, interest):
    # определяем вероятности попадения в блоки гистограммы
    hist = [0] * bins
    for (x, y) in interest:
        hist[int(img[x][y] / step)] += 1
    for i in range(bins):
        hist[i] /= len(interest)
    return hist


class image2graph:
    def __init__(self, img, obj, bkg, lambda_const=1, sigma_const=1):
        self.lambda_const = lambda_const
        self.sigma_const = sigma_const
        self.img = img
        self.number_of_nodes = len(img.ravel())
        self.number_of_rows = len(img)
        self.number_of_cols = len(img[0])
        self.obj_probs = generate_probs(img, obj)
        self.bkg_probs = generate_probs(img, bkg)
        self.obj_set = set(obj)
        self.bkg_set = set(bkg)
        self.obj_terminal, self.bkg_terminal = self.number_of_nodes, self.number_of_nodes+1
        graph = Graph(n=self.number_of_nodes+2, source=self.obj_terminal, target=self.bkg_terminal)
        for i in range(self.number_of_rows):
            for j in range(self.number_of_cols):
                if (i, j) in self.obj_set:
                    graph.add_edge(self.obj_terminal, self.number_of_cols * i + j, K)
                    graph.add_edge(self.number_of_cols * i + j, self.bkg_terminal, 1e-15)
                elif (i, j) in self.bkg_set:
                    graph.add_edge(self.obj_terminal, self.number_of_cols * i + j, 0)
                    graph.add_edge(self.number_of_cols*i + j, self.bkg_terminal, K)
                else:
                    R_obj = -np.log(min(self.obj_probs[img[i][j] // step] + epsilon, 1))
                    R_bkg = -np.log(min(self.bkg_probs[img[i][j] // step] + epsilon, 1))
                    graph.add_edge(self.obj_terminal, self.number_of_cols*i + j, lambda_const*R_bkg)
                    graph.add_edge(self.number_of_cols*i + j, self.bkg_terminal, lambda_const*R_obj)
                intensity = img[i][j]
                if i > 0:
                    other_intensity = img[i-1][j]
                    weight = np.exp(-((int(intensity)-int(other_intensity))**2) / (2 * (sigma_const**2)))
                    graph.add_edge(self.number_of_cols*i + j, self.number_of_cols*(i-1) + j, weight)
                if i < self.number_of_rows-1:
                    other_intensity = img[i+1][j]
                    weight = np.exp(-((int(intensity) - int(other_intensity)) ** 2) / (2 * (sigma_const ** 2)))
                    graph.add_edge(self.number_of_cols * i + j, self.number_of_cols * (i+1) + j, weight)
                if j > 0:
                    other_intensity = img[i][j-1]
                    weight = np.exp(-((int(intensity) - int(other_intensity)) ** 2) / (2 * (sigma_const ** 2)))
                    graph.add_edge(self.number_of_cols * i + j, self.number_of_cols*i + j - 1, weight)
                if j < self.number_of_cols-1:
                    other_intensity = img[i][j+1]
                    weight = np.exp(-((int(intensity) - int(other_intensity)) ** 2) / (2 * (sigma_const ** 2)))
                    graph.add_edge(self.number_of_cols * i + j, self.number_of_cols*i + j + 1, weight)
        self.graph = graph

    def min_cut(self):
        self.graph.dinic()
        return self.graph.min_cut()

    def change_to_obj(self, vertex):
        vertex_idx = vertex[0]*self.number_of_cols + vertex[1]
        R_obj = -np.log(min(self.obj_probs[self.img[vertex[0]][vertex[1]] // step] + epsilon, 1))
        R_bkg = -np.log(min(self.bkg_probs[self.img[vertex[0]][vertex[1]] // step] + epsilon, 1))
        self.graph.add_to_edge(self.obj_terminal, vertex_idx, K+self.lambda_const*R_obj)
        self.graph.add_to_edge(vertex_idx, self.bkg_terminal, self.lambda_const*R_bkg)

    def change_to_bkg(self, vertex):
        vertex_idx = vertex[0] * self.number_of_cols + vertex[1]
        R_obj = -np.log(min(self.obj_probs[self.img[vertex[0]][vertex[1]] // step] + epsilon, 1))
        R_bkg = -np.log(min(self.bkg_probs[self.img[vertex[0]][vertex[1]] // step] + epsilon, 1))
        self.graph.add_to_edge(self.obj_terminal, vertex_idx, self.lambda_const * R_obj)
        self.graph.add_to_edge(vertex_idx, self.bkg_terminal, K + self.lambda_const * R_bkg)

