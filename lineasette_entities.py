# Single item (identified by its code)
class Item:
    def __init__(self, code, price, dimension):
        self._code = code
        self._price = price
        self._dimension = dimension
    
    @property
    def code(self):
        return self._code

    @property
    def price(self):
        return self._price

    @property
    def dimension(self):
        return self._dimension

# Family of items (identified by the prefix of its items' codes)
class Family:
    def __init__(self, code, items, name, image):
        self._code = code
        self._items = items
        self._name = name
        self._image = image

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def items(self):
        return self._items

    @property
    def image(self):
        return self._image