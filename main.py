from PIL import Image, ImageDraw
import numpy as np
import random


class Creation:
    def __init__(self, w, h, r, g, b):
        # create an image with a base color and load the pixels
        self.w = w  # width
        self.h = h  # height
        self.image = Image.new(mode="RGB", size=(self.w, self.h), color=(r, g, b))
        self.pixels = self.image.load()

    def scatter(self, count, meanx, meany, stdevx, stdevy, r, g, b):
        for i in range(count):
            x = round(np.random.normal(meanx, stdevx))
            y = round(np.random.normal(meany, stdevy))
            try:
                self.pixels[x, y] = r, g, b
            except:
                i -= 1  # didnt work, will try again

    def conway(self, dr, dg, db, ar, ag, ab):  # dead rgb or alive rgb
        og = self.image.copy()
        og_pix = og.load()
        for x in range(self.w):
            for y in range(self.h):
                alive = False
                if og_pix[x, y] == (ar, ag, ab):
                    alive = True
                alive_around = 0
                # find how many around are alive
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if not (i == 0 and j == 0):
                            try:
                                if og_pix[x+i, y+j] == (ar, ag, ab):
                                    alive_around += 1
                            except:
                                pass
                # these are directly the rules of Conway's Game of Life
                try:
                    if alive:
                        # if there are less than two alive around live cell, it dies
                        if alive_around < 2:
                            self.pixels[x, y] = dr, dg, db
                        # if a live cell has more than three neighbours, it dies
                        elif alive_around > 3:
                            self.pixels[x, y] = dr, dg, db
                        # if a live cell has 2 or 3 live neighbours, it stays alive
                        elif 2 <= alive_around <= 3:
                            pass  # nothing happens, its alive and stays so
                    else:
                        # if there are exactly three alive around it, a dead one becomes alive
                        if int(alive_around) == 3:
                            self.pixels[x, y] = ar, ag, ab
                except:
                    pass

    def life_without_death(self, dr, dg, db, ar, ag, ab):  # dead rgb or alive rgb
        og = self.image.copy()
        og_pix = og.load()
        for x in range(self.w):
            for y in range(self.h):
                alive = False
                if og_pix[x, y] == (ar, ag, ab):
                    alive = True
                alive_around = 0
                # find how many around are alive
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if not (i == 0 and j == 0):
                            try:
                                if og_pix[x+i, y+j] == (ar, ag, ab):
                                    alive_around += 1
                            except:
                                pass
                # these are directly the rules of Conway's Game of Life
                try:
                    if alive:
                        pass
                        # no death
                    else:
                        # if there are exactly three alive around it, a dead one becomes alive
                        if int(alive_around) == 3:
                            self.pixels[x, y] = ar, ag, ab
                except:
                    pass

    def diamoeba(self, dr, dg, db, ar, ag, ab):  # dead rgb or alive rgb
        og = self.image.copy()
        og_pix = og.load()
        for x in range(self.w):
            for y in range(self.h):
                alive = False
                if og_pix[x, y] == (ar, ag, ab):
                    alive = True
                alive_around = 0
                # find how many around are alive
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if not (i == 0 and j == 0):
                            try:
                                if og_pix[x + i, y + j] == (ar, ag, ab):
                                    alive_around += 1
                            except:
                                pass

                try:
                    if alive:
                        if alive_around in [5, 6, 7, 8]:
                            pass  # nothing happens, its alive and stays so
                        else:
                            self.pixels[x, y] = dr, dg, db
                    else:
                        if alive_around in [3, 5, 6, 7, 8]:
                            self.pixels[x, y] = ar, ag, ab
                except:
                    pass

    def cloud(self, feature_size, color, octaves, persistence, seed):
        for x in range(self.w):
            for y in range(self.h):
                noise_value = noise.snoise2(x=x / feature_size / octaves,
                                            y=y / feature_size / octaves,
                                            persistence=persistence,
                                            octaves=octaves,
                                            base=seed
                                            )
                background_color = self.pixels[x, y]
                intensity = float((noise_value+1)/2)
                self.pixels[x, y] = tuple(np.round(np.add(np.multiply(intensity, np.array(color)),
                                                 np.multiply((1-intensity), np.array(background_color)))))

    def save(self, title):
        self.image.save(str(title) + ".png")


# def main():
#     e = Creation(300, 300, 0, 0, 0)
#     e.scatter(15000, 100, 60, 255, 255, 255)
#     for i in range(1, 300):
#         e.diamoeba(0, 0, 0, 255, 255, 255)
#         if i%20 == 0:
#             e.scatter(4000, i, 15+(i/10), 255, 255, 255)
#         e.save(i)

def main():
    e = Creation(200, 200, 0, 0, 0)
    e.scatter(10000, 100, 20, 255, 255, 255)
    for i in range(1, 400):
        e.conway(0, 0, 0, 255, 255, 255)
        if i%20 == 0:
            e.scatter(1000, i/2, 10, 255, 255, 255)
        e.save(i)


add = []


def banner():
    for j in range(10):
        banner_map = Creation(240, 120, 0, 0, 0)
        for i in range(0, 600):
            if i%601 == 0:
                banner_map.scatter(20000, 120, 60, 1000, 60, 160, 160, 160)
            banner_map.conway(0, 0, 0, 160, 160, 160)
            new_img = banner_map.image.copy()
            up_scale = new_img.resize((960, 480), resample=Image.BOX)
            # make bigger, don't AA
            add.append(up_scale)
    add[0].save("240 banner 4x.gif", save_all=True, append_images=add[1:], optimize=True, duration=100, loop=0)


banner()