import os

from PIL import Image

# Given an image (RGBA), return:
# last_transparent_row_top,
# last_transparent_row_bottom,
# last_transparent_column_left,
# last_transparent_column_right
def _get_box(img):
    w, h = img.size
    pixels = list(img.getdata())
    result = [-1, h, -1, w]
    for index, iterable in enumerate([range(h), reversed(range(h)), range(w), reversed(range(w))]):
        for i in iterable:
            vec = pixels[w*i:w*(i+1)] if index < 2 else [pixels[idx*w+i] for idx in range(h)]
            print(min([pixel[3] for pixel in vec]))
            if max([pixel[3] for pixel in vec]) == 0:
                result[index] = i
            else:
                break
    return result

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