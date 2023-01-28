from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt 
from flask_app.models.user import User
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'users_id' not in session:
        return render_template('index.html')
    else:
        return redirect('/dashboard')

@app.route('/register', methods=['POST'])
def register():
        isValid = User.validate_register(request.form)
        if not isValid:
            return redirect('/')
        newUser = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.save(newUser)
        if not id:
            flash('Something went wrong')
            return redirect('/')
        else:
            session['user_id'] = id
            flash("you are now logged in")
            return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.get_by_email(data)
    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    else:
        session['users_id'] = user.id
        return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')