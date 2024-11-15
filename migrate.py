import sqlite3

from vista import VistaHelper

vista = VistaHelper("profile.data")
conn = sqlite3.connect("profile.db")
cur = conn.cursor()

# Create table with key (varchar, max 250, not null primary key) and value (text)
cur.execute("CREATE TABLE IF NOT EXISTS ProductCatalog (Key VARCHAR(250) PRIMARY KEY NOT NULL, Value TEXT)")

# Get all keys from Vista
data = vista.get_key_value_list("SELECT * FROM ProductCatalog")
for key, value in data:
    cur.execute("INSERT INTO ProductCatalog (Key, Value) VALUES (?, ?)", (key, value))

conn.commit()
