import pandas as pd

# Convert the price list from .xsl to .csv
def xls_to_csv(xls_file, csv_file):
    data_xls = pd.read_excel(xls_file, converters={"PREZZO": lambda price: "{0:.2f}".format(price)}, index_col=None)
    data_xls.to_csv(csv_file, encoding='utf-8', index=False)