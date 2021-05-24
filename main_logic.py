import math
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Dinic import Graph

# infinity edge
K = 2
lambda_const = 10
sigma_const = 1
epsilon = 1e-6

def generate_obj_bkg_scribbles():
    # эмитирует то, что мы отметили как фон и обьект
    obj = []
    for i in range(150, 175):
        obj.append((i, 50 + 2*(i-150)))
        obj.append((i, 50 + 2*(i-150)+1))
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


def generate_probs(img, interest, bins=15):
    # определяем вероятности попадения в блоки гистограммы
    step = math.ceil(256//bins)
    probs = [0] * bins
    for (x, y) in interest:
        probs[img[x][y] // step] += 1
    for i in range(bins):
        probs[i] /= len(interest)
    return probs


def image2graph(img, obj, bkg, obj_probs, bkg_probs):
    number_of_nodes = len(img.ravel())
    number_of_rows = len(img)
    number_of_cols = len(img[0])
    obj_set = set(obj)
    bkg_set = set(bkg)
    graph = Graph(n=number_of_nodes+2, source=-1, target=number_of_nodes)
    for i in range(number_of_rows):
        for j in range(number_of_cols):
            # 25 from number of bins, epsilon for not to take ln(0)
            if (i, j) in obj_set:
                graph.add_edge(-1, number_of_cols * i + j, K)
                graph.add_edge(number_of_cols * i + j, number_of_nodes, 0)
            elif (i, j) in bkg_set:
                graph.add_edge(-1, number_of_cols * i + j, 0)
                graph.add_edge(number_of_cols*i + j, number_of_nodes, K)
            else:
                R_obj = -np.log(obj_probs[img[i][j] // 25] + epsilon)
                R_bkg = -np.log(bkg_probs[img[i][j] // 25] + epsilon)
                graph.add_edge(-1,              number_of_cols*i + j, lambda_const*R_bkg)
                graph.add_edge(number_of_cols*i + j, number_of_nodes, lambda_const*R_obj)
            intensity = img[i][j]
            if i > 0:
                other_intensity = img[i-1][j]
                graph.add_edge(number_of_cols*i + j, number_of_cols*(i-1) + j,
                               np.exp((-1 / (2 * (sigma_const**2))) * (int(intensity)-int(other_intensity))**2))
            if i < number_of_rows-1:
                other_intensity = img[i+1][j]
                graph.add_edge(number_of_cols * i + j, number_of_cols * (i+1) + j,
                               np.exp((-1 / (2 * (sigma_const ** 2))) * (int(intensity) - int(other_intensity)) ** 2))
            if j > 0:
                other_intensity = img[i][j-1]
                graph.add_edge(number_of_cols * i + j, number_of_cols*i + j - 1,
                               np.exp((-1 / (2 * (sigma_const ** 2))) * (int(intensity) - int(other_intensity)) ** 2))
            if j < number_of_cols-1:
                other_intensity = img[i][j+1]
                graph.add_edge(number_of_cols * i + j, number_of_cols*i + j + 1,
                               np.exp((-1 / (2 * (sigma_const ** 2))) * (int(intensity) - int(other_intensity)) ** 2))
    return graph


img = mpimg.imread('./images/banana1-gr-320.jpg')
obj_scribble, bkg_scribble = generate_obj_bkg_scribbles()

obj_probs = generate_probs(img, obj_scribble)
bkg_probs = generate_probs(img, bkg_scribble)

underlying_graph = image2graph(img, obj_scribble, bkg_scribble, obj_probs, bkg_probs)
start = time.time()
flow = underlying_graph.dinic()
end = time.time()
print("Time in seconds", "%.3f" % (end - start))
print('Max flow: ', flow)
