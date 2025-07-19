from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = 'freezer.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/test")
def test_api():
    return jsonify({"message": "API is working!"})

@app.route("/products", methods=["GET"])
def get_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY program ASC, name ASC")
    products = cursor.fetchall()
    conn.close()
    return jsonify([dict(product) for product in products])

def initialize_database():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        program INTEGER NOT NULL,
                        name TEXT NOT NULL NULL,
                        quantity INTEGER NOT NULL NULL DEFAULT 0,
                        order_warning INTEGER NOT NULL DEFAULT 0,
                        serial TEXT NOT NULL)''')
    conn.commit()

    # Check if table is empty before inserting
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''INSERT INTO products (name, program, quantity, serial) VALUES (?, ?, ?, ?)''', [
            ('Ice Cream', 10, 0, "00000"),
            ('Frozen Vegetables', 20, 8, "00001"),
            ('Frozen Pizza', 15, 19, "00002"),
            ('Frozen Rucola', 15, 19, "00003")
        ])
        conn.commit()
    
    conn.close()

if __name__ == '__main__':
    print("Initializing database...")
    initialize_database()
    print("Backend is up")
    app.run(host="0.0.0.0", port=7001)
