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


scribbles = [generate_scribbles_0_3, generate_scribbles_0_3, generate_scribbles_0_3, generate_scribbles_0_3,
             generate_scribbles_4, generate_scribbles_5, generate_scribbles_6]
