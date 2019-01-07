from glob import glob
from enum import Enum
from lineasette_entities import Family, Item
from PIL import Image
from xml.etree.ElementTree import Element

import os
import pandas as pd
import re

# Possible proportions each Container could have
class Proportions(Enum):
    QUADRATO = (1, 1)
    RETT1 = (1.5, 1)
    RETT2 = (1, 1.5)

    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def ratio(self):
        return self.width/self.height

# Possible dimensions each Container could have
class Dimensions(Enum):
    GRANDE = 2.0
    MEDIA = 1.5
    PICCOLA = 1.0

# HTML representation of a Family
class Container:
    def __init__(self, family):
        self._family = family
        img = Image.open(family.image)
        w, h = img.size
        self._dimension = Dimensions.PICCOLA if w==833 or h==833 else Dimensions.MEDIA if w==1250 or h==1250 else Dimensions.GRANDE
        self._proportion = Proportions.QUADRATO if w==h else Proportions.RETT1 if w>h else Proportions.RETT2

    @property
    def family(self):
        return self._family

    @property
    def dimension(self):
        return self._dimension

    @property
    def proportion(self):
        return self._proportion

    @property
    def width(self):
        return self.proportion.width * self.dimension.value * 37.79

    @property
    def height(self):
        return self.proportion.height * self.dimension.value * 37.79

    def _details_column(self):
        details_column = Element("div", {"class": "details-column"})
        details_column.append(Element("img", {"src": os.path.join("images", os.path.basename(self.family.image)), "style": "width:{}px;height:{}px;".format(self.width, self.height)}))
        description_element = Element("div", {"class": "description"})
        name_element = Element("div", {"class": "name"})
        name_element.text = self.family.name
        description_element.append(name_element)
        codes_element = Element("div", {"class": "codes"})
        for item in self.family.items:
            code_element = Element("div", {"class": "code"})
            code_element.text = item.code
            codes_element.append(code_element)
        description_element.append(codes_element)
        details_column.append(description_element)
        return details_column

    def _dimension_column(self):
        dimension_column = Element("div", {"class": "dimension-column"})
        for item in self.family.items:
            dimension_element = Element("div", {"class": "dimension"})
            dimension_element.text = item.dimension
            dimension_column.append(dimension_element)
        return dimension_column

    def _price_column(self):
        price_column = Element("div", {"class": "price-column"})
        for item in self.family.items:
            price_element = Element("div", {"class": "price"})
            price_element.text = str(item.price)
            price_column.append(price_element)
        return price_column

    def xml_element(self):
        element = Element("div", {"class": "{} {}".format(self.proportion.name, self.dimension.name)})
        element.append(self._details_column())
        element.append(self._dimension_column())
        element.append(self._price_column())
        return element

# Return a list of containers, given the csv file and the images folder
def get_containers(csv_file, images_folder):
    print("Generating a list of containers...")
    containers = []
    data = pd.read_csv(csv_file, dtype={"PREZZO": str})
    for list, list_items in data.groupby(["LISTA"], sort=True):
        list_containers = []
        for container_info, items_df in list_items.groupby(["FAMIGLIA", "DESCRIZIONE"]):
            items = []
            for index, row in items_df.iterrows():
                items.append(Item(row["CODICE"], row["PREZZO"], row["DIMENSIONE"]))
            family_image = glob(os.path.join(images_folder, "{}.png".format(container_info[0])))[0]
            family = Family(container_info[0], items, container_info[1], family_image)
            list_containers.append(Container(family))
        list_containers.sort(key=lambda container: 
                                    (re.findall("^[A-Za-z]+", container.family.code)[0],
                                    int(re.findall("[0-9]+", container.family.code)[0]),
                                    re.findall("[A-Za-z]*$", container.family.code)))
        containers += list_containers
    print("{} containers have been successfully generated:".format(len(containers)))
    containers_str = ""
    for container in containers[:-1]:
        containers_str += "{}, ".format(container.family.code)
    containers_str += containers[-1].family.code
    print(containers_str)
    return containers