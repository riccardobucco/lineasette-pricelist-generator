from enum import Enum
from xml.etree.ElementTree import Element

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
    PICCOLA = 1.0

# HTML representation of a Family
class Container:
    def __init__(self, family, dimension):
        self._family = family
        self._dimension = Dimensions.__members__[dimension.upper()]
        self._proportion = Proportions.__members__[family.image.rstrip(".png").rsplit("-", 1)[1].upper()]

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
        details_column.append(Element("img", {"src": self.family.image, "style": "width:{}px;height:{}px;".format(self.width, self.height)}))
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
    containers = []
    data = pd.read_csv(csv_file, dtype={"PREZZO": str})
    for container_info, items_df in data.groupby(["FAMIGLIA", "DESCRIZIONE", "DIMENSIONE IMMAGINE"]):
        items = []
        for index, row in items_df.iterrows():
            items.append(Item(row["CODICE"], row["PREZZO"], row["DIMENSIONE"]))
        family_image = glob(os.path.join(images_folder, "{}-*.png".format(container_info[0])))[0]
        family = Family(container_info[0], items, container_info[1], family_image)
        containers.append(Container(family, container_info[2]))
    containers.sort(key=lambda container: container.family.code)
    return containers