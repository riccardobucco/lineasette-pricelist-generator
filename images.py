import os

from PIL import Image

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