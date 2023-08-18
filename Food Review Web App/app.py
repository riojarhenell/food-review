from flask import Flask, render_template, request, flash, session, redirect, url_for, escape
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'my_secret_key'

app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "food_review_py"

mysql = MySQL(app)

@app.route("/", methods=['GET','POST'])

def index():

    mycursor = mysql.connection.cursor()

    mycursor.execute("SELECT * FROM users")

    result = mycursor.fetchall()

    return render_template('index.html', result=result)

@app.route("/about", methods=['GET','POST'])

def about():

    return render_template('about.html')

@app.route("/register", methods=['GET','POST'])

def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        salt = "SaLt"
        db_password = password+salt
        hash_password = sha256_crypt.encrypt(db_password)

        mycursor = mysql.connection.cursor()

        mycursor.execute("SELECT * FROM users WHERE username = (%s)", (username,))
        user_username = mycursor.fetchone()

        if user_username:
            flash('Username already taken', 'error')
            return render_template('register.html')
        else:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            val = (username, hash_password)
            mycursor.execute(sql, val)
            mysql.connection.commit()
            mycursor.close()
            flash('User added successfully!', 'success')
            return render_template('register.html')
        
    return render_template('register.html')

@app.route("/login", methods=['GET','POST'])

def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Login Failed.', 'error')
            return render_template('login.html')
        
        salt = "SaLt"
        db_password = password+salt
        sha256_crypt.encrypt(db_password)

        mycursor = mysql.connection.cursor()

        mycursor.execute("SELECT * FROM users WHERE username = (%s)", (username,))
        user_username = mycursor.fetchone()

        if user_username:
            password_db = user_username[2] 
            verify = sha256_crypt.verify(db_password, password_db)
            if verify is True:
                flash('Logging in...', 'success')
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                flash('Login Failed. Please check your password then try again.', 'error')
                return render_template('login.html')
        else:
            flash('Login Failed. Please check your username and password then try again.', 'error')
            return render_template('login.html')
        
    return render_template('login.html')

@app.route("/logout", methods=['GET','POST'])

def logout():

    session.pop('username', None)
    return redirect(url_for('login'))



#Custom Error Pages
#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)