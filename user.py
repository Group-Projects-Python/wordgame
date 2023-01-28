from flask_app.confi.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = ['first_name']
        self.last_name = ['last_name']
        self.email = ['email']
        self.password = ['password']
        self.score = ['score']
        self.created_at = ['created_at']
        self.updated_at = ['updated_at']
    db = "word_guess"

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, score) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(score)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        isvalid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            isvalid= False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email", "register")
            isvalid= False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            isvalid= False
        if len(user['last_name']) < 2:
            flash("First name must be a least 2 characters", "register")
            isvalid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            isvalid= False
        if user['password'] != user['confirm']:
            flash("Password don't match", "register")
        return isvalid
