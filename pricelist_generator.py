from configparser import ConfigParser
from containers import get_containers
from gui import get_user_input
from math import ceil, floor
from shutil import copyfile
from utilities import get_margin, xls_to_csv
from xml.etree.ElementTree import Element, tostring

import os
import requests
import tkinter as tk
import xml.dom.minidom

PIXELS_PER_CM = 37.79

def _partition(A, h):
    """
    Computes a partition of the element of A based on the height h.
    Returns the tuple (number of columns, element-column assignment).
    """
    I = []
    if len(A) == 0:
        return 0, I

    n = 1
    curr_h = 0

    for a in A:
        if curr_h + a > h:
            n += 1
            curr_h = 0

        curr_h += a
        I.append(n-1)

    return n, I

def _ceil(c, m):
    """
    Returns the ceil of the given number c to the next multiple of m.
    """
    return int(m * ceil(float(c) / m))

def _get_solution(m, h, A):
    """
    Computes the solution of the problem, where m is the multiplier column's
    factor, h is the height of the column, A is an array of element's height.
    """
    c, I = _partition(A, h)
    maxcol = _ceil(c, m)

    while c <= maxcol:
        h -= 1
        c, I = _partition(A, h)

    h += 1

    c, I = _partition(A, h)
    return I, c

# Create the head of the html price list
def _head():
    head = Element("head")
    head.append(Element("meta", {"charset": "UTF-8"}))
    head.append(Element("link", {"rel": "stylesheet", "href": "listino.css"}))
    title = Element("title")
    title.text = "Listino"
    head.append(title)
    return head

# Create a column of the html price list
def _body_column(containers, margin):
    tot = 0
    column = Element("div", {"class": "column"})
    if len(containers) == 1:
        item = containers[0].xml_element()
        item.set("class", "{} {}".format(item.get("class"), "column-first-container"))
        details_colum = item.find("./div[@class='details-column']")
        details_colum.set("style", "margin-top:{}px;margin-bottom:{}px;".format(margin, margin)) #TODO
        column.append(item)
        return column
    item = containers[0].xml_element()
    item.set("class", "{} {}".format(item.get("class"), "column-first-container"))
    item.set("style", "height:{}px".format(containers[0].height))
    tot += containers[0].height
    column.append(item)
    for it in containers[1:-1]:
        item = it.xml_element()
        details_colum = item.find("./div[@class='details-column']")
        item.set("style", "flex-grow: 1;")
        tot += it.height + margin*2
        column.append(item)
    item = containers[-1].xml_element()
    item.set("class", "{} {}".format(item.get("class"), "column-last-container"))
    tot += containers[-1].height + margin*2
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
    page = Element("div", {"class": "page", "style": "height: {}".format(COLUMN_HEIGHT)})
    for i in range(num_columns):
        margin = get_margin(containers_heights[solution.index(i) : len(solution) - list(reversed(solution)).index(i)], COLUMN_HEIGHT)
        max_containers = solution.count(i)
        column = _body_column(containers[first_unused_container:first_unused_container + max_containers], margin)
        page.append(column)
        first_unused_container += max_containers
        columns_count += 1
        if columns_count == MAX_COLUMNS:
            break_page = Element("div", {"style": "page-break-before:always;"})
            body.append(page)
            page = Element("div", {"class": "page"})
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
    if layout == 0:
        COLUMN_HEIGHT = 18 * PIXELS_PER_CM
        MAX_COLUMNS = 4
    elif layout == 1:
        COLUMN_HEIGHT = 26 * PIXELS_PER_CM
        MAX_COLUMNS = 3
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
