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


def generate_scribbles_4():
    obj = generate_rect((40, 55), 60, 3)
    obj += generate_interval((98, 160), (131, 212), 3)
    bkg = generate_rect((14, 47), 4, 69)
    bkg += generate_rect((240, 78), 4, 69)
    return obj, bkg

def generate_scribbles_5():
    obj = generate_rect((281, 155), 60, 8)
    obj += generate_interval((102, 147), (132, 200), 4)
    bkg = generate_rect((114, 15), 5, 69)
    bkg += generate_rect((257, 268), 99, 7)
    return obj, bkg

def generate_scribbles_6():
    obj = generate_rect((71, 218), 60, 8)
    obj += generate_interval((60, 113), (91, 166), 4)
    bkg = generate_rect((114, 15), 5, 69)
    return obj, bkg

def generate_scribbles_7():
    obj = generate_rect((297, 152), 60, 8)
    obj += generate_interval((39, 131), (61, 184), 4)
    bkg = generate_rect((130, 267), 99, 7)
    bkg += generate_rect((291, 29), 5, 69)
    return obj, bkg

def generate_scribbles_8():
    obj = generate_rect((285, 91), 60, 8)
    obj += generate_interval((156, 158), (180, 211), 4)
    bkg = generate_rect((14, 27), 99, 7)
    bkg += generate_rect((104, 299), 70, 5)
    return obj, bkg

def generate_scribbles_9():
    obj = generate_rect((77, 128), 60, 8)
    bkg = generate_rect((110, 18), 99, 7)
    bkg += generate_rect((104, 299), 70, 5)
    return obj, bkg

def generate_scribbles_11():
    obj = generate_rect((96, 150), 60, 8)
    bkg = generate_rect((110, 18), 99, 7)
    bkg += generate_rect((104, 299), 70, 5)
    return obj, bkg

def generate_scribbles_12():
    obj = generate_rect((190, 175), 60, 8)
    bkg = generate_rect((114, 79), 99, 7)
    bkg += generate_rect((220, 285), 70, 5)
    bkg += generate_rect((32, 50), 70, 5)
    return obj, bkg

def generate_scribbles_13():
    obj = generate_rect((102, 122), 60, 14)
    bkg = generate_rect((32, 39), 70, 5)
    bkg += generate_rect((88, 280), 99, 7)
    return obj, bkg

def generate_scribbles_14():
    obj = generate_rect((130, 141), 200, 14)
    bkg = generate_rect((151, 273), 99, 8)
    return obj, bkg

def generate_scribbles_15():
    obj = generate_rect((30, 145), 160, 14)
    bkg = generate_rect((60, 26), 99, 8)
    return obj, bkg

def generate_scribbles_16():
    obj = generate_rect((67, 165), 86, 8)
    obj += generate_interval((207, 274), (232, 205), 8)
    obj += generate_rect((185, 168), 4, 25)
    bkg = generate_rect((75, 45), 99, 8)
    return obj, bkg

def generate_scribbles_17():
    obj = generate_rect((82, 168), 86, 8)
    obj += generate_interval((225, 246), (235, 219), 8)
    obj += generate_rect((232, 135), 4, 25)
    bkg = generate_rect((75, 45), 99, 8)
    return obj, bkg

def generate_scribbles_18():
    obj = generate_rect((138, 204), 25, 3)
    obj += generate_interval((295, 168), (306, 142), 4)
    obj += generate_rect((165, 125), 4, 19)
    obj += generate_rect((213, 172), 4, 19)
    bkg = generate_rect((204, 37), 99, 8)
    bkg += generate_rect((17, 255), 99, 8)
    return obj, bkg

def generate_scribbles_19():
    obj = generate_rect((55, 175), 4, 19)
    obj += generate_rect((139, 201), 69, 4)
    bkg = generate_rect((32, 24), 99, 8)
    bkg += generate_rect((47, 283), 99, 8)
    bkg += generate_rect((74, 93), 99, 8)
    return obj, bkg

def generate_scribbles_20():
    obj = generate_rect((146, 106), 69, 4)
    bkg = generate_rect((313, 184), 99, 8)
    bkg += generate_rect((22, 89), 66, 5)
    return obj, bkg

def generate_scribbles_21():
    obj = generate_interval((144, 142), (257, 153), 4)
    bkg = generate_rect((320, 237), 99, 8)
    bkg += generate_interval((36, 129), (84, 84), 5)
    bkg += generate_rect((99, 41), 99, 8)
    return obj, bkg

def generate_scribbles_22():
    obj = generate_interval((129, 148), (242, 160), 4)
    bkg = generate_rect((59, 58), 99, 8)
    bkg += generate_rect((227, 281), 99, 8)
    return obj, bkg

def generate_scribbles_23():
    obj = generate_rect((69, 164), 120, 4)
    bkg = generate_rect((76, 296), 99, 8)
    bkg += generate_rect((59, 58), 99, 8)
    return obj, bkg

def generate_scribbles_24():
    obj = generate_rect((84, 180), 4, 20)
    obj += generate_rect((126, 96), 4, 20)
    bkg = generate_rect((109, 225), 99, 8)
    return obj, bkg

def generate_scribbles_25():
    obj = generate_rect((135, 164), 99, 8)
    bkg = generate_rect((308, 85), 4, 31)
    return obj, bkg

def generate_scribbles_26():
    obj = generate_rect((90, 181), 99, 8)
    bkg = generate_rect((152, 32), 4, 60)
    return obj, bkg

def generate_scribbles_28():
    obj = generate_interval((177, 156), (279, 183), 8)
    bkg = generate_rect((136, 27), 4, 62)
    return obj, bkg

def generate_scribbles_29():
    obj = generate_rect((160, 160), 83, 3)
    bkg = generate_interval((61, 29), (195, 89), 4)
    return obj, bkg


scribbles = [generate_scribbles_0_3, generate_scribbles_0_3, generate_scribbles_0_3, generate_scribbles_0_3,
             generate_scribbles_4, generate_scribbles_5, generate_scribbles_6, generate_scribbles_7,
             generate_scribbles_8, generate_scribbles_9, generate_scribbles_9, generate_scribbles_11,
             generate_scribbles_12, generate_scribbles_13, generate_scribbles_14, generate_scribbles_15,
             generate_scribbles_16, generate_scribbles_17, generate_scribbles_18, generate_scribbles_19,
             generate_scribbles_20, generate_scribbles_21, generate_scribbles_22, generate_scribbles_23,
             generate_scribbles_24, generate_scribbles_25, generate_scribbles_26, generate_scribbles_26,
             generate_scribbles_28, generate_scribbles_29]
