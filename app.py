from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__,static_url_path='/static')

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="passwords"
)
cursor = conn.cursor()

# Define routes

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_credentials(username, password):
            return redirect(url_for('menu'))
        else:
            return "Invalid username or password."
    return render_template('login.html', error=error)

@app.route('/menu')
def menu():
    return render_template("menu.html")

@app.route('/add_password', methods=['POST','GET'])
def add_password():
    if(request.method == 'GET'):
        return render_template('addpassword.html')
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']
        add_password_to_db(website, username, password)
        return redirect(url_for('index'))  # Redirect back to the home page after adding password

@app.route('/get_password', methods=['POST','GET'])
def get_password():
    if(request.method == 'GET'):
        return render_template('getpassword.html')
    if request.method == 'POST':
        website = request.form['website']
        cursor.execute('''SELECT password FROM passwordtable WHERE website=%s''', (website,))
        password = cursor.fetchone()
        if password:
            return render_template('last.html', password=password[0])
            #return f"Password for {website}: {password[0]}"
        else:
            return "No password found for this website."
    return render_template("getpassword.html")

def verify_credentials(username, password):
    cursor.execute('''SELECT * FROM login WHERE username = %s AND password = %s''', (username, password))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False

def add_password_to_db(website, username, password):
    sql = '''INSERT INTO passwordtable (website, username, password) VALUES (%s, %s, %s)'''
    val = (website, username, password)
    cursor.execute(sql, val)
    conn.commit()

if __name__ == '__main__':
    app.run(debug=True)

# Close connection to database
conn.close()
