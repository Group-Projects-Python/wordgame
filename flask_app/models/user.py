# Wordle Reloaded Project

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DB = "word_guess"
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.score = data['score']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_user_by_email(cls,user_email):
        data = {"email":user_email}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query,data)
        print("get by email = ",results)
        if len(results) < 1 :
            return False
        return cls(results[0])
    
    @classmethod
    def add_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,score,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,0,NOW(),NOW());"
        results = connectToMySQL(DB).query_db(query,data)
        return results
    
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users ORDER BY score DESC;"
        results = connectToMySQL(DB).query_db(query)
        all_users=[]
        for each_user in results:
            all_users.append(cls(each_user))
        return all_users
    
    @classmethod
    def update_score(cls,data):
        query = "UPDATE users SET score=%(score)s WHERE id=%(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        return result
    
    @classmethod
    def get_score_by_id(cls,id):
        data = {
            "id":id
        }
        query = "SELECT score FROM users WHERE id=%(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        print("Get Score by ID method = ",result[0])
        return result[0]
    
    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        print("Get user by ID method = ",result[0])
        return cls(result[0])

    @classmethod
    def update_user(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,password=%(password)s WHERE id=%(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        print("Update result = ",result)
        return result

    @classmethod
    def delete_user(cls,id):
        data = {
            "id":id
        }
        query = "DELETE FROM users WHERE id=%(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        return result

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name should have atleast 2 Characters","register")
            is_valid = False
        if len(user['last_name']) < 2 :
            flash("Last Name should have atleast 2 Characters","register")
            is_valid = False
        if len(user['email']) == 0 :
            flash("Email cannot be empty","register")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address","register")
            is_valid = False
        if len(user['password']) < 8 :
            flash("Password should have atleast 8 Characters","register")
            is_valid = False
        if len(user['confirm_password']) < 8 :
            flash("Confirm Password should have atleast 8 Characters","register")
            is_valid = False
        if not (user['password'] == user['confirm_password']) :
            flash("Password and Confirm Password is NOT matching","register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['email']) == 0 :
            flash("Email cannot be empty","login")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address","login")
            is_valid = False
        if len(user['password']) == 0 :
            flash("Password cannot be empty","login")
            is_valid = False
        return is_valid