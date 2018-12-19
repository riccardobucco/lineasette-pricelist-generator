from constraint_solver import get_solution
from containers import get_containers
from math import ceil, floor
from utilities import get_margin, xls_to_csv
from xml.etree.ElementTree import Element, tostring

import xml.dom.minidom

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
        details_colum = item.find("./div[@class='details-column']")
        details_colum.set("style", "margin-top:{}px;margin-bottom:{}px;".format(margin, margin))
        column.append(item)
        return column
    item = containers[0].xml_element()
    details_colum = item.find("./div[@class='details-column']")
    tot += containers[0].height
    column.append(item)
    for it in containers[1:-1]:
        item = it.xml_element()
        details_colum = item.find("./div[@class='details-column']")
        details_colum.set("style", "margin-top:{}px;".format(margin*2))
        tot += it.height + margin*2
        column.append(item)
    item = containers[-1].xml_element()
    tot += containers[-1].height + margin*2
    details_colum = item.find("./div[@class='details-column']")
    details_colum.set("style", "margin-top:{}px;".format(margin*2))
    column.append(item)
    return column

# Create the body of the html price list
def _body(containers):
    containers_heights = [container.height for container in containers]
    solution, num_columns = get_solution(MULT, floor(COLUMN_HEIGHT), [ceil(h) for h in containers_heights])
    body = Element("body")
    first_unused_container = 0
    columns_count = 0
    page = Element("div", {"class": "page"})
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

if __name__ == "__main__":
    xls_to_csv("listino.xls", "listino.csv")
    xml_string = xml.dom.minidom.parseString(tostring(listino("listino.csv", "./images")))
    with open("listino.html", "w") as file:
        file.write(xml_string.toprettyxml())