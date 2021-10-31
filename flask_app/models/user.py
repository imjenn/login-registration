#import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 

# regex object
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Class methods to query db

    # C - Create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('login').query_db(query, data)

    # R - Read/Retrieve all
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('login').query_db(query)
        all_users = []
        for user in results:
            all_users.append(cls(user))
        return all_users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # R - Read/Retrieve one
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL('login').query_db(query, data)
        return cls(results[0])

    # Regex static method
    @staticmethod
    def is_valid(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login').query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if user['pw1'] != user['pw2']:
            flash("Passwords do not match.")
        return is_valid