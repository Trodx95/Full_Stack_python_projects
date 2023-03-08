# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt
from flask import flash, session 
import re
    # from flask_app import DATABASE 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = "exam_shows_db"

    # model the class after the friend users from our database 
class User:
    def __init__(self , data):
        # ADD attributes for every column in our database users 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']
        self.full_name = f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
        

    # C
    @classmethod 
    def create(cls, data:dict) -> int:
        #add all column names and add all values
        query = "INSERT INTO users (first_name, last_name, email, pw) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw)s);"
        #return me the id/row of the new user added to the database
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id

    # R
    @classmethod 
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False 
        
    @classmethod 
    def get_one_by_email(cls, data:dict) -> list:
        
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False 

    @classmethod 
    def get_all(cls) -> list:
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(users))
            return all_users
        return False

    # UPDATE
    @classmethod 
    def update_one(cls, data:dict) -> None:
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email= %(email)s WHERE id = %(id)s;"
        return connectToMySQL(DATEBASE).query_db(query, data)

    # DELETE
    @classmethod 
    def delete_one(cls , data:dict) -> None:
        # ADD COLUMNS = values for every column that you wish to change in to db
        query= "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # REGISTRATION
    @staticmethod
    def validator(data:dict) -> bool:
        print("here")
        is_valid = True 

        if len(data['first_name']) < 1:
            flash('First name must be atleast 2 characters' , 'err_user_first_name')
            is_valid = False
        
        if len(data['last_name']) < 1:
            flash('Last name must be atleast 2 characters' , 'err_user_last_name')
            is_valid = False
        
        if len(data['email']) < 1:
            flash('Valid Email format, that does not already exist in the database' , 'err_user_email')
            is_valid = False
        
        elif not EMAIL_REGEX.match(data['email']): 
            flash('Invalid email address!', 'err_user_email')
            is_valid = False
        else:
            potential_user = User.get_one_by_email({'email' : data['email']})
            if potential_user:
                flash('Email already in use', 'err_user_email')
                is_valid = False

            
        
        if len(data['pw']) < 1:
            flash('At least 8 characters' , 'err_user_pw')
            is_valid = False
        if len(data['confirm_pw']) < 1:
            flash('needs to match password' , 'err_user_confirm_pw')
            is_valid = False
        elif data['pw'] != data['confirm_pw']:
            flash('Passwords do not match', 'err_user_confirm_pw')
            is_valid = False
        
        return is_valid 

    @staticmethod
    # LOGIN VALIDATOR
    def validator_login(data:dict) -> bool:
        
        is_valid = True 
        
        if len(data['email']) < 1:
            flash('Valid Email format, that does not already exist in the database' , 'err_user_email_login')
            is_valid = False
        
        elif not EMAIL_REGEX.match(data['email']): 
            flash('Invalid email address!', 'err_user_email_login')
            is_valid = False
        else:
            potential_user = User.get_one_by_email({'email' : data['email']})
            if not potential_user:
                flash('invalid Credentials!', 'err_user_email_login')
                is_valid = False
        
            #check the hash 
            elif not bcrypt.check_password_hash(potential_user.pw, data['pw']):
                flash('invalid credentials!!', 'err_user_email_login')
                is_valid = False
            else:
            # store id into session 
                session['uuid'] = potential_user.id
            

        
        if len(data['pw']) < 1:
            flash('field is required' , 'err_user_pw_login')
            is_valid = False
        
        
        return is_valid 