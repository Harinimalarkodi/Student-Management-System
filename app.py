from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"


# -------------------------
# DATABASE
# -------------------------
def init_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        department TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
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
# STUDENT REGISTER
# -------------------------
@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        password = request.form['password']

        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO students(name,email,department,password) VALUES(?,?,?,?)",
        (name,email,department,password)
        )

        conn.commit()
        conn.close()

        return redirect('/student_login')

    return render_template('register.html')


# -------------------------
# STUDENT LOGIN
# -------------------------
@app.route('/student_login', methods=['GET','POST'])
def student_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM students WHERE email=? AND password=?",
        (email,password)
        )

        student = cursor.fetchone()

        conn.close()

        if student:
            session['student'] = email
            return redirect('/student_dashboard')
        else:
            return "Invalid Login"

    return render_template('student_login.html')


# -------------------------
# STUDENT DASHBOARD
# -------------------------
@app.route('/student_dashboard')
def student_dashboard():

    if 'student' not in session:
        return redirect('/student_login')

    return render_template('student_dashboard.html')


# -------------------------
# SUBMIT FEEDBACK
# -------------------------
@app.route('/submit', methods=['POST'])
def submit():

    if 'student' not in session:
        return redirect('/student_login')

    name = request.form['name']
    roll = request.form['roll']
    rating = request.form['rating']
    comments = request.form['comments']

    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO feedback(name,roll,rating,comments) VALUES(?,?,?,?)",
    (name,roll,rating,comments)
    )

    conn.commit()
    conn.close()

    return render_template('thankyou.html')


# -------------------------
# ADMIN LOGIN
# -------------------------
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')


# -------------------------
# ADMIN AUTH
# -------------------------
@app.route('/admin_auth', methods=['POST'])
def admin_auth():

    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "1234":
        session['admin'] = True
        return redirect('/admin')
    else:
        return "Invalid Credentials"


# -------------------------
# ADMIN DASHBOARD
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
# VIEW FEEDBACK
# -------------------------
@app.route('/view')
def view():

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM feedback")
    data = cursor.fetchall()

    conn.close()

    return render_template('view.html', data=data)


# -------------------------
# LOGOUT
# -------------------------
@app.route('/logout')
def logout():

    session.pop('student', None)
    session.pop('admin', None)

    return redirect('/')


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)