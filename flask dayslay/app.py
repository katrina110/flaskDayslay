from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None 

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid email or password. Please try again.'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None  # Initialize error variable
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            error = 'Username already exists. Please choose another username.'
        elif existing_email:
            error = 'Email address already in use. Please use a different email address.'
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            session['logged_in'] = True
            return redirect(url_for('index'))

    return render_template('register.html', error=error)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
