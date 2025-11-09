from flask import Flask, render_template, request, redirect
import sqlite3
import os
from datetime import date

app = Flask(__name__)

# Use /tmp for serverless environments (Vercel, AWS Lambda, etc.)
# In local development, use habits.db in the project directory
def get_db_path():
    if os.path.exists('/tmp'):
        return '/tmp/habits.db'
    return 'habits.db'

def init_db():
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        last_done TEXT,
                        streak INTEGER
                    )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

@app.route('/')
def index():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    habits = conn.execute('SELECT * FROM habits').fetchall()
    conn.close()
    return render_template('index.html', habits=habits)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        conn.execute('INSERT INTO habits (name, last_done, streak) VALUES (?, ?, ?)',
                     (name, '', 0))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

@app.route('/done/<int:id>')
def done(id):
    today = str(date.today())
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    habit = conn.execute('SELECT * FROM habits WHERE id=?', (id,)).fetchone()
    if habit and habit[2] != today:
        streak = habit[3] + 1
        conn.execute('UPDATE habits SET last_done=?, streak=? WHERE id=?',
                     (today, streak, id))
        conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
