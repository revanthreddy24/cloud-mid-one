
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('todos.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT NOT NULL)')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form['task']
        if task:
            conn = get_db_connection()
            conn.execute('INSERT INTO todos (task) VALUES (?)', (task,))
            conn.commit()
            conn.close()
            return redirect('/')
    
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
