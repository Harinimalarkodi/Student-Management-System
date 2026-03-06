from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"


# -------------------------
# Create Database Table
# -------------------------
def init_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll TEXT,
            rating TEXT,
            comments TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# -------------------------
# HOME PAGE
# -------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -------------------------
# SUBMIT FEEDBACK
# -------------------------
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    roll = request.form['roll']
    rating = request.form['rating']
    comments = request.form['comments']

    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (name, roll, rating, comments) VALUES (?, ?, ?, ?)",
        (name, roll, rating, comments)
    )
    conn.commit()
    conn.close()

    return render_template('thankyou.html')


# -------------------------
# PUBLIC VIEW PAGE
# -------------------------
@app.route('/view')
def view():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    data = cursor.fetchall()
    conn.close()

    return render_template('view.html', data=data)


# -------------------------
# ADMIN LOGIN PAGE
# -------------------------
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')


# -------------------------
# ADMIN AUTHENTICATION
# -------------------------
@app.route('/admin_auth', methods=['POST'])
def admin_auth():
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "1234":
        session['admin'] = True
        return redirect('/admin')
    else:
        return "Invalid credentials"


# -------------------------
# ADMIN PAGE (PROTECTED)
# -------------------------
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/admin_login')

    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    data = cursor.fetchall()
    conn.close()

    return render_template('admin.html', data=data)


# -------------------------
# LOGOUT
# -------------------------
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')


# -------------------------
# RUN APP
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)