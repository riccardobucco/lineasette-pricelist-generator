from PIL import Image

import math
import os
import pandas as pd

# Convert the price list from .xsl to .csv
def xls_to_csv(xls_file, csv_file):
    data_xls = pd.read_excel(xls_file, converters={"PREZZO": lambda price: "{0:.2f}".format(price)}, index_col=None)
    data_xls.to_csv(csv_file, encoding='utf-8', index=False)

# Resize images in in_folder, saving them in out_folder
def make_images(in_folder, out_folder):
    for file in os.listdir(in_folder):
        img = Image.open(os.path.join(in_folder, file))
        w, h = img.size
        new_img = img.resize((math.floor(w/4), math.floor(h/4)), Image.ANTIALIAS)
        new_img.save(os.path.join(out_folder, file))