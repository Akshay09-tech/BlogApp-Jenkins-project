from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # ← yeh add karo

def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, content TEXT)')
    conn.commit()
    conn.close()

@app.route('/add', methods=['POST'])
def add_post():
    data = request.json
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (content) VALUES (?)', (data['content'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Post added"})

@app.route('/posts', methods=['GET'])
def get_posts():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts')
    posts = c.fetchall()
    conn.close()
    return jsonify(posts)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
