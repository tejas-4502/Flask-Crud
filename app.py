from flask import Flask, render_template, request, redirect, url_for
import sqlite3
 
app = Flask(__name__)
 
# Database initialization
 
def init_db():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
 
    # Create user table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT NOT NULL,
            email TEXT NOT NULL,
            mobno TEXT NOT NULL
        )
    ''')
 
    conn.commit()
    conn.close()
 
# database
init_db()

# nav base
@app.route('/')
def login():
    return render_template('index.html')
 
# Create
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        mobno = request.form['mobno']
 
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
 
        # Insert data
        cursor.execute('INSERT INTO user (name, age, email, mobno) VALUES (?, ?, ?, ?)', (name, age, email, mobno))
 
        conn.commit()
        conn.close()
 
        return redirect(url_for('get_users'))
 
    return render_template('add.html')
 
# Read
@app.route('/users')
def get_users():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
 
    # Fetch all data
    cursor.execute('SELECT * FROM user')
    users = cursor.fetchall()
 
    conn.close()
 
    return render_template('users.html', users=users)
 
# Update
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
 
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        mobno = request.form['mobno']
 
        # Update data
        cursor.execute('UPDATE user SET name=?, age=?, email=?, mobno=? WHERE id=?', (name, age, email, mobno, id))
 
        conn.commit()
        conn.close()
 
        return redirect(url_for('get_users'))
    else:
        # Fetch the data by id
        cursor.execute('SELECT * FROM user WHERE id=?', (id,))
        user = cursor.fetchone()
 
        conn.close()
 
        return render_template('edit.html', user=user)
 
# Delete
@app.route('/delete/<int:id>')
def delete_user(id):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
 
    # Delete the by id
    cursor.execute('DELETE FROM user WHERE id=?', (id,))
 
    conn.commit()
    conn.close()
 
    return redirect(url_for('get_users'))
 
if __name__ == '__main__':
    app.run(debug=True)