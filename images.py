import math
import numpy as np
import os

from PIL import Image

# Given an image (RGBA), return:
# last_transparent_column_left,
# last_transparent_row_top,
# last_transparent_column_right,
# last_transparent_row_bottom
def _get_box(img):
    w, h = img.size
    pixels = list(img.getdata())
    result = [-1, -1, w, h]
    for index, iterable in enumerate([range(w), range(h), reversed(range(w)), reversed(range(h))]):
        for i in iterable:
            vec = pixels[w*i:w*(i+1)] if index==1 or index==3 else [pixels[idx*w+i] for idx in range(h)]
            if max([pixel[3] for pixel in vec]) == 0:
                result[index] = i
            else:
                break
    return result

# Align the images in in_folder according to x and y, saving them in out_folder
# 
#        x
#        ------
#        -1 0 1
#        ------
# y |-1 | A B C
#   | 0 | D E F
#   | 1 | G H I
def align_images(x, y, in_folder, out_folder=None):
    for file in os.listdir(in_folder):
        img = Image.open(os.path.join(in_folder, file))
        img = img.convert("RGBA")
        w, h = img.size
        box = _get_box(img)
        print(box)
        img = img.crop((box[0]+1, box[1]+1, box[2]-1, box[3]-1))
        n_empty_rows = (box[1] + 1) + (h - box[3] + 1)
        n_empty_columns = (box[0] + 1) + (w - box[2] + 1)
        value = np.empty((), dtype=np.dtype("int,int,int,int"))
        value[()] = (255, 255, 255, 0)
        margin_left = np.full((img.size[1], 0 if x==-1 else math.floor(n_empty_columns/2) if x==0 else n_empty_columns), value)
        margin_right = np.full((img.size[1], n_empty_columns if x==-1 else math.ceil(n_empty_columns/2) if x==0 else 0),
                               value)
        margin_top = np.full((0 if y==-1 else math.floor(n_empty_rows/2) if y==0 else n_empty_rows, w),
                             value)
        margin_bottom = np.full((n_empty_rows if y==-1 else math.ceil(n_empty_rows/2) if y==0 else 0, w),
                                value)
        pixels = list(img.getdata())
        pixels = np.array(pixels, dtype=np.dtype("int,int,int,int")).reshape((img.size[1], img.size[0]))
        pixels = np.hstack((margin_left, pixels, margin_right))
        pixels = np.vstack((margin_top, pixels, margin_bottom))
        pixels = pixels.reshape(-1).tolist()
        img = Image.new(img.mode, (w,h))
        img.putdata(pixels)
        if out_folder is None:
            img.save(os.path.join(in_folder, file))
        else:
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)
            img.save(os.path.join(out_folder, file))

# Remove all the white pixels of the images in in_folder, saving them in out_folder
def white2transparent(in_folder, out_folder=None):
    for file in os.listdir(in_folder):
        img = Image.open(os.path.join(in_folder, file))
        img = img.convert("RGBA")
        pixels = img.getdata()
        new_pixels = []
        for pixel in pixels:
            if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
                new_pixels.append((255, 255, 255, 0))
            else:
                new_pixels.append(pixel)
        img.putdata(new_pixels)
        if out_folder is None:
            img.save(os.path.join(in_folder, file))
        else:
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)
            img.save(os.path.join(out_folder, file))