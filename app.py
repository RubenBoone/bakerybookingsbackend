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
    return "API link is working!"
if __name__ == '__main__':
    print("Backend is up")
    app.run(host="0.0.0.0", port=7001)