import json

# from vista import VistaHelper
import sqlite3

from flask import Flask, jsonify, request

from Archive import Archive

# from BinaryReaderCustom import BinaryReader
from slpp import slpp as lua

app = Flask(__name__)

archive = Archive.open("inventory.data")
# vista = VistaHelper("profile.data")
db = sqlite3.connect("profile.db", check_same_thread=False)
cur = db.cursor()


@app.route("/lookup/barcode/<barcode>", methods=["GET"])
def lookup_barcode(barcode: str):
    print(f"Looking up barcode: {barcode}")
    index = archive.find_index(barcode)
    if index:
        item = archive.read_inventory(index)
        # strip total_rental_count
        item.pop("total_rental_count")
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


@app.route("/lookup/product/id/<pid>", methods=["GET"])
def lookup_product_by_id(pid: int):
    print(f"Looking up product: {pid}")
    cur.execute("SELECT [Value] FROM ProductCatalog WHERE [Key] = ?", (pid,))
    product = cur.fetchone()
    if product:
        data = lua.decode(product[0])
        print(data)
        return jsonify(data)
    return jsonify({"error": "Product not found"}), 404


@app.route("/lookup/product/barcode/<barcode>", methods=["GET"])
def lookup_product_by_barcode(barcode: str):
    print(f"Looking up product by barcode: {barcode}")
    index = archive.find_index(barcode)
    if index:
        item = archive.read_inventory(index)
        # get title_id
        title_id = item["title_id"]
        cur.execute("SELECT [Value] FROM ProductCatalog WHERE [Key] = ?", (title_id,))
        product = cur.fetchone()
        if product:
            data = lua.decode(product[0])
            return jsonify(data)
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"error": "Barcode not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
