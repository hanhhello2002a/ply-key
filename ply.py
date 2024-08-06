from flask import Flask, request, jsonify
import sqlite3
import random
import string

app = Flask(__name__)

# Tạo cơ sở dữ liệu và bảng nếu chưa tồn tại
def setup_database():
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            key TEXT PRIMARY KEY,
            used_on TEXT
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

def generate_random_key(length=16):
    """Tạo key ngẫu nhiên với chiều dài nhất định"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/add_random_key', methods=['POST'])
def add_random_key():
    data = request.json
    used_on = data.get('used_on')
    if not used_on:
        return jsonify({"error": "Invalid data"}), 400

    key = generate_random_key()
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO keys (key, used_on) VALUES (?, ?)', (key, used_on))
    conn.commit()
    conn.close()
    return jsonify({"key": key, "message": "Key added successfully"}), 201

@app.route('/delete_key', methods=['DELETE'])
def delete_key():
    data = request.json
    key = data.get('key')
    if not key:
        return jsonify({"error": "Key is required"}), 400

    conn = sqlite3.connect('keys.db')
    c = conn.cursor()
    c.execute('DELETE FROM keys WHERE key = ?', (key,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Key deleted successfully"}), 200

@app.route('/get_keys', methods=['GET'])
def get_keys():
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()
    c.execute('SELECT * FROM keys')
    rows = c.fetchall()
    conn.close()
    return jsonify({"keys": rows})

if __name__ == '__main__':
    app.run(debug=True)
