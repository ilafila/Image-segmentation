import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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


img = mpimg.imread('./images/banana1-gr-320.jpg')
obj_scribble, bkg_scribble = generate_obj_bkg_scribbles()

obj_probs = generate_probs(img, obj_scribble)
bkg_probs = generate_probs(img, bkg_scribble)

print(obj_probs)
print(bkg_probs)


