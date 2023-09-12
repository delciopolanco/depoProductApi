import csv
import os
from models.product import Product
from models.webTypes import WebTypes
from services.database.dbProducts import DBProducts

def saveFileInfo(search: Product, fileName: str):
    
    directory_path = './build'  # Path to the one-level-above directory

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = f'{directory_path}/{fileName}.csv'
    f = open(file_path, 'a', newline='')
    row = (search.description, search.store, search.currency, search.price)
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()

def saveDBInfo(product: Product):
    
    db = DBProducts()
    db.insert(product)