# Login Registration Assignment
# Author: Vignesh Manickam

from flask_app import app
from flask import render_template,request,redirect,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
import requests

bcrypt = Bcrypt(app)
words_tried=[]

# Base Route
@app.route("/")
def base():
    return render_template("login.html")

# User Registration Route
@app.route("/register",methods=['POST'])
def register():
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "confirm_password" : request.form['confirm_password'],
    }
    if User.validate_registration(data):
        data["password"] = bcrypt.generate_password_hash(request.form['password'])
        data["confirm_password"] = bcrypt.generate_password_hash(request.form['confirm_password'])
        result = User.add_user(data)
        session['user_name'] = data['first_name']
        session['user_id'] = result
    else :
        return redirect("/")
    return redirect("/dashboard")

# Login Route
@app.route("/login",methods=['POST'])
def login():
    data = {
        "email" : request.form['email'],
        "password": request.form['password']
    }
    print(data)
    if User.validate_login(data):
        print("inside user validation")
        user_detail = User.get_user_by_email(data['email'])
        if not user_detail:
            flash("invalid email","login")
            return redirect('/')
        if not bcrypt.check_password_hash(user_detail.password,request.form['password']):
            print("inside pwd check validation")
            flash("wrong password","login")
            return redirect('/')
        session['user_name'] = user_detail.first_name
        session['user_id'] = user_detail.id
        print("Returing dashboard")
        return redirect('/dashboard')
    else:
        return redirect('/')

# Dashboard Route
@app.route("/dashboard")
def home():
    if (session.get('user_id') != None ):
        session['attempt']=0
        session['score']=500
        response = requests.get("https://random-word-api.herokuapp.com/word?length=5")
        print(response.status_code)
        print(response.json())
        data = response.json()
        print(data[0])
        return render_template("home.html",word=data[0])
    else :
        return redirect('/')

# Validation Route
# This route will compare the string entered by the user with random word generated and provide the results
@app.route("/validate",methods=['POST'])
def validate():
    user_word=""
    box_style=[]
    # Incrementing the attempt count
    session['attempt'] = session['attempt'] + 1
    # Reading the values from the form - Which is entered on the screen
    data = {
        "first": request.form['first'],
        "second":request.form['second'],
        "third":request.form['third'],
        "fourth":request.form['fourth'],
        "fifth":request.form['fifth']
    }
    # Reading the random word picked by Python random.choice method from home route
    word_random = request.form['word']
    print("inside validate")
    print("Random word = ",word_random)
    print("User entered value = ",data)
    # Reading the values from Dictionary and concatenating each letter into a word
    for each_key in data :
        user_word = user_word+data[each_key]
    # Converting both random word and user entered word to lowercase for string comparison
    word_random = word_random.lower()
    user_word = user_word.lower()
    # Comparing the strings
    # On Success Route to Dashboard
    if (user_word == word_random):
        print("Success")
        return redirect('/leaderboard')
    else :
        if session['attempt'] == 6 :
            pass # Write a flask message of correct word.
        # On Failure - Check each character against random word and provide result
        # Reduce the score for every attempt
        session['score'] = session['score'] - 50
        if (len(word_random) == len(user_word)) :
            for i in range(len(user_word)) :
                print("Comparing",word_random[i],user_word[i])
                if (word_random[i] == user_word[i]):
                    #print("Green")
                    box_style.append("Green")
                elif (user_word[i] in word_random):
                    #print("Yellow")
                    box_style.append("Yellow")
                else:
                    box_style.append("Red")
                    #print("Red")
    print("REsulting Style = ",box_style)
    # Add the tried words into array to display it on HTML Page
    words_tried.append(user_word)
    return render_template("validate.html",box_list=box_style,user_entry=data,word=word_random,word_list=words_tried)

# This Route is to enable the user to try for another word guess
@app.route("/another",methods=['POST'])
def play():
    print(len(words_tried))
    # Clearing the words tried array, as it was a new word guess
    words_tried.clear()
    print("After clear",len(words_tried))
    return redirect('/dashboard')

# Leaderboard Route
@app.route("/leaderboard")
def leaderboard():
    print("Inside Dashboard")
    data = {
        "id":session['user_id'],
        "score":session['score']
    }
    result = User.update_score(data)
    print(result)
    user_list = User.get_all_users()
    return render_template("leaderboard.html",users_list=user_list)

# Route to Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
