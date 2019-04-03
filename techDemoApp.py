# Importing Flask form Python's Flask library
import os
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt # Used for password encryption
from functools import wraps

app = Flask(__name__)
# Can be used to run the app in debug mode so we won't have to restart server
#app.debug = True

# Config mySQL (Google: flask mysql seetup)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' # WILL VARY FOR EACH USER AND HOW THEIR MYSQL IS SETUP
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'GSWTechDemoFlask'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # Use dictionary
# init mySQL
mysql = MySQL(app)

#Articles = Articles()

# Check if user is logged in
def is_logged_in(f):
    # From Python wraps library
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Home Page
# Page Not Found will show up if this is not defined
@app.route('/')
def index():
    return render_template('home.html')

# Articles page
@app.route('/articles')
@is_logged_in
def articles():
    # Create cusror
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    # Fetches all articles in dictionary format
    articles = cur.fetchall()
    print articles
    # Display maessage if no results found
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)

    # Close connection
    cur.close()

# Single Article page
@app.route('/article/<string:id>/')
@is_logged_in
def article(id):
    # Create cusror
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()

    return render_template('article.html', article=article)

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# User Registration Form Class (Registration uses wtforms library)
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match.')
    ])
    confirm = PasswordField('Confirm Password')

# User Registration page
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)

    cur = mysql.connection.cursor()

    #Check if username is taken or not
    username = str(form.username.data)
    result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

    if result > 0:
         error = 'Username already exists'
         return render_template('home.html', error=error)

    else:
     # if not then proceed with registeration. 
        if request.method == 'POST' and form.validate():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password.data))

            # Create cursor
            cur = mysql.connection.cursor()

            # Execute query
            cur.execute("INSERT INTO users(name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, password))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            flash ('Your user registration is complete and can now log in!', 'success')

            return redirect(url_for('index'))


    # Return template and pass in the form we just created above
    return render_template('register.html', form=form)

# Login page (login functionality and page takes place here)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form fields for login Page
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get started hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Password valid (uses session library from Flask)
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in!', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid password entered'
                #return redirect(url_for('login', error=error))
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            # For debugging purposes (prints to terminal)
            #app.logger.info('NO USER')
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Logout page
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# Dashboard page
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cusror
    cur = mysql.connection.cursor()

    # Get articles for the logged in user (if any found)
    result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])

    # Fetches all articles in dictionary format
    articles = cur.fetchall()

    # Display message if no results found
    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)

    # Close connection
    cur.close()

# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add Article page
@app.route('/add_article', methods=['GET','POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Article Created Successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)

# Edit article
@app.route('/edit_article/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get aritcle by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()

    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id = %s", (title, body, [id]))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Article Updated Successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute query
    cur.execute("DELETE FROM articles WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()

    flash('Article Deleted Successfully', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    app.secret_key='cmpt470'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
