# Wordle Project

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
DB = "word_guess"
class Score:
    def __init__(self,data) :
        self.id = data['id']
        self.score = data['score']
        self.word = data['word']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def add_score(cls,data):
        query = "INSERT INTO scores (score,user_id,word,created_at,updated_at) VALUES %(score)s,%(user_id)s,%(word)s,NOW(),NOW();"
        result = connectToMySQL(DB).query_db(query,data)
        return result
    
    @classmethod
    def display_score(cls):
        query = "SELECT * FROM scores;"
        result = connectToMySQL(DB).query_db(query)
        all_scores=[]
        for row in result:
            all_scores.append(cls(row))
        return all_scores