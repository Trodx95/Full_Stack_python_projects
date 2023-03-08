# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app import DATABASE
from flask import flash

from flask_app.models import model_user


DATABASE ="exam_shows_db"
    # model the class after the friend table from our database 
class Show:
    def __init__(self , data):
        # ADD attributes for every column in our database table 
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.user_id = data['user_id']
        # self.updated_at = data['updated_at']
        
        

    # C
    @classmethod 
    def create(cls, data:dict) -> int:
        #add all column names and add all values
        query = "INSERT INTO shows (title, network , release_date,  description, user_id) VALUES ( %(title)s, %(network)s, %(release_date)s,  %(description)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # R
    @classmethod 
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False 


    
    @classmethod 
    def get_one_by_id(cls, data:dict) -> list:
        query = "SELECT * FROM shows JOIN users ON users.id = shows.user_id WHERE shows.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        show = cls(result[0])
        row_from_db = result[0]
        user_data = {
                    **row_from_db,
                    'id': row_from_db['users.id'],
                    'first_name': row_from_db['first_name'],
                    'last_name': row_from_db['last_name'],
                    'email': row_from_db['email'],
                    'pw': row_from_db['pw'],
                    
            }
        owner = model_user.User(user_data)
        show.chef = owner 
        return show
        


    @classmethod 
    def get_all(cls) -> list:
        query = "SELECT * FROM shows JOIN users ON users.id = shows.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        if results:
            all_shows = []
            for dict in results:
                show = cls(dict)
                user_data = {
                    'id': dict['users.id'],
                    'first_name': dict['first_name'],
                    'last_name': dict['last_name'],
                    'email': dict['email'],
                    'pw': dict['pw'],
                    
                }
                user = model_user.User(user_data)
                show.chef = user
                all_shows.append((show))
            return all_shows
        return []


                

    # Update
    @classmethod 
    def update_one(cls, data:dict) -> None:
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # Delete
    @classmethod 
    def delete_one(cls , data:dict) -> None:
        # ADD COLUMNS = values for every column that you wish to change in to db
        query= "DELETE FROM shows WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)
    # Validations 
    @staticmethod
    def validator(data:dict) -> bool:
        is_valid = True

        if len(data['title']) < 1:
            flash('field is required must be atleast 3 characters' , 'err_shows_name')
            is_valid = False
        
        if len(data['network']) < 1:
            flash('field is required must be atleast 3 characters' , 'err_shows_network')
            is_valid = False
        
        if len(data['release_date']) < 1:
            flash('field is required' , 'err_shows_release_date')
            is_valid = False

        if len(data['description']) < 1:
            flash('field is required must be atleast 3 characters' , 'err_shows_description')
            is_valid = False
        
        

        #some code logic here

        return is_valid 
