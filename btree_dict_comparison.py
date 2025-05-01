from BTrees.OOBTree import OOBTree
import timeit
import csv
import os

# Path
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "generated_items_data.csv")


# Generate data
def load_products_from_csv(file_path):
    products = []
    with open(file_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            product = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"]),
            }
            products.append(product)
    return products


# Initialize structs
tree = OOBTree()
dictionary = {}


# Functions to add items
def add_item_to_tree(tree, product):
    tree[product["ID"]] = product


def add_item_to_dict(d, product):
    d[product["ID"]] = product


# Functions to query by price range
def range_query_tree(tree, min_price, max_price):
    return [item for item in tree.values() if min_price <= item["Price"] <= max_price]


def range_query_dict(d, min_price, max_price):
    return [item for item in d.values() if min_price <= item["Price"] <= max_price]


# Load from CSV
products = load_products_from_csv(file_path)

# Populate
for product in products:
    add_item_to_tree(tree, product)
    add_item_to_dict(dictionary, product)

# Timeit setup
min_price, max_price = 100, 300
setup_tree = "from __main__ import range_query_tree, tree, min_price, max_price"
stmt_tree = "range_query_tree(tree, min_price, max_price)"
setup_dict = "from __main__ import range_query_dict, dictionary, min_price, max_price"
stmt_dict = "range_query_dict(dictionary, min_price, max_price)"

# Measure 100 executions for each function
time_tree = timeit.timeit(stmt=stmt_tree, setup=setup_tree, number=100)
time_dict = timeit.timeit(stmt=stmt_dict, setup=setup_dict, number=100)

print(f"Total range_query time for OOBTree: {time_tree:.6f} seconds")
print(f"Total range_query time for Dict: {time_dict:.6f} seconds")
