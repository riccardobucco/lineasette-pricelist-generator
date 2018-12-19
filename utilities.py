import pandas as pd

# Convert the price list from .xsl to .csv
def xls_to_csv(xls_file, csv_file):
    data_xls = pd.read_excel(xls_file, converters={"PREZZO": lambda price: "{0:.2f}".format(price)}, index_col=None)
    data_xls.to_csv(csv_file, encoding='utf-8', index=False)

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