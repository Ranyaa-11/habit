from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    last_done TEXT,
                    streak INTEGER
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('habits.db')
    habits = conn.execute('SELECT * FROM habits').fetchall()
    conn.close()
    return render_template('index.html', habits=habits)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        conn = sqlite3.connect('habits.db')
        conn.execute('INSERT INTO habits (name, last_done, streak) VALUES (?, ?, ?)',
                     (name, '', 0))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

@app.route('/done/<int:id>')
def done(id):
    today = str(date.today())
    conn = sqlite3.connect('habits.db')
    habit = conn.execute('SELECT * FROM habits WHERE id=?', (id,)).fetchone()
    if habit[2] != today:
        streak = habit[3] + 1
        conn.execute('UPDATE habits SET last_done=?, streak=? WHERE id=?',
                     (today, streak, id))
        conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
