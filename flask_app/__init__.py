# Word Game Project
# Author: Vignesh Manickam

from flask import Flask,session

app = Flask(__name__)
app.secret_key = "LoginSecret"