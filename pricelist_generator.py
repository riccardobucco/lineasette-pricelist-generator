from configparser import ConfigParser
from containers import get_containers
from gui import get_user_input
from math import ceil, floor
from shutil import copyfile
from utilities import make_images, xls_to_csv
from xml.etree.ElementTree import Element, tostring

import os
import requests
import tkinter as tk
import xml.dom.minidom

PIXELS_PER_CM = 37.79
HORIZONTAL_HEIGHT = 18
VERTICAL_HEIGHT = 26

def _get_solution(mult, column_height, heights):
    data = {"mult": mult,
            "column_height": column_height,
            "heights": str(heights).replace(" ", "").lstrip("[").rstrip("]")}
    r = requests.post(URL_CP_SOLVER, data=data)
    result = r.json()
    return result["solution"], result["num_columns"]

# Create the head of the html price list
def _head():
    head = Element("head")
    head.append(Element("meta", {"charset": "ISO-8859-1"}))
    head.append(Element("link", {"rel": "stylesheet", "href": "listino.css"}))
    title = Element("title")
    title.text = "Listino"
    head.append(title)
    return head

# Create a column of the html price list
def _body_column(containers):
    tot = 0
    column = Element("div", {"class": "column {}".format(LAYOUT)})
    # TODO: Test the case in which a column has only one container
    if len(containers) == 1:
        item = containers[0].xml_element()
        item.set("class", "{} {}".format(item.get("class"), "column-first-container"))
        details_colum = item.find("./div[@class='details-column']")
        column.set("style", "justify-content:center;align-items:center;")
        column.append(item)
        return column
    item = containers[0].xml_element()
    item.set("class", "{} {}".format(item.get("class"), "column-first-container"))
    item.set("style", "flex-grow: 1".format(containers[0].height))
    column.append(item)
    for it in containers[1:-1]:
        item = it.xml_element()
        details_colum = item.find("./div[@class='details-column']")
        item.set("style", "flex-grow: 1;")
        column.append(item)
    item = containers[-1].xml_element()
    item.set("class", "{} {}".format(item.get("class"), "column-last-container"))
    details_colum = item.find("./div[@class='details-column']")
    item.set("style", "flex-grow: 1;")
    column.append(item)
    return column

# Create the body of the html price list
def _body(containers):
    containers_heights = [container.height for container in containers]
    print("Computing the layout...")
    solution, num_columns = _get_solution(MULTIPLE, floor(COLUMN_HEIGHT), [ceil(h) for h in containers_heights])
    print("COMPUTED LAYOUT:")
    print("- Number of columns: {}".format(num_columns))
    print("- Solution:")
    for c in range(num_columns):
        print("  Column n.{}:".format(c))
        c_sol = [j for j, sol in enumerate(solution) if sol==c]
        c_sol_str = ""
        for i in c_sol[:-1]:
            c_sol_str += "{}, ".format(containers[i].family.code)
        c_sol_str += containers[c_sol[-1]].family.code
        print("  {}".format(c_sol_str))
    body = Element("body")
    first_unused_container = 0
    columns_count = 0
    page = Element("div", {"class": "page {}".format(LAYOUT)})
    for i in range(num_columns):
        max_containers = solution.count(i)
        column = _body_column(containers[first_unused_container:first_unused_container + max_containers])
        page.append(column)
        first_unused_container += max_containers
        columns_count += 1
        if columns_count == MAX_COLUMNS:
            break_page = Element("div", {"style": "page-break-before:always;"})
            body.append(page)
            page = Element("div", {"class": "page {}".format(LAYOUT)})
            columns_count = 0
    if page.find("./div") is not None:
        body.append(page)
    return body

# Create an html price list from the given containers
def _html(containers):
    html = Element("html")
    html.append(_head())
    html.append(_body(containers))
    return html

# Convert a csv file to a price list
def listino(csv_file, images_folder):
    containers = get_containers(csv_file, images_folder)
    return _html(containers)

# Main function
def main(layout, multiple, pricelist_filename, images_location, save_location):
    global COLUMN_HEIGHT
    global MAX_COLUMNS
    global MULTIPLE
    global LAYOUT
    if layout == 0:
        COLUMN_HEIGHT = HORIZONTAL_HEIGHT * PIXELS_PER_CM
        MAX_COLUMNS = 4
        LAYOUT = "horizontal"
    elif layout == 1:
        COLUMN_HEIGHT = VERTICAL_HEIGHT * PIXELS_PER_CM
        MAX_COLUMNS = 3
        LAYOUT = "vertical"
    MULTIPLE = multiple
    print("Layout: {}".format("horizontal" if layout==1 else "vertical"))
    print("Pricelist: {}".format(pricelist_filename))
    print("Images location: {}".format(images_location))
    print("Save location: {}".format(save_location))
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    print("Converting the pricelist into a .csv file...")
    xls_to_csv(pricelist_filename, os.path.join("tmp", "listino.csv"))
    xml_string = xml.dom.minidom.parseString(tostring(listino(os.path.join("tmp", "listino.csv"), images_location)))
    print("Saving the pricelist as a .html file...")
    save_location = os.path.join(save_location, "listino")
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    with open(os.path.join(save_location, "listino.html"), "w") as file:
        file.write(xml_string.toprettyxml())
    if not os.path.exists(os.path.join(save_location, "images")):
        os.makedirs(os.path.join(save_location, "images"))
    print("Resizing images...")
    make_images(images_location, os.path.join(save_location, "images"))
    copyfile(os.path.join("res", "listino.css"), os.path.join(save_location, "listino.css"))
    print("Removing temporary files...")
    os.remove(os.path.join("tmp", "listino.csv"))
    print("Pricelist successfully generated!")
    input("Press ENTER to continue...")

if __name__ == "__main__":
    config = ConfigParser()
    config.read(os.path.join("res", "config.ini"))
    URL_CP_SOLVER = config["cpsolver"]["url"]
    get_user_input(main)
