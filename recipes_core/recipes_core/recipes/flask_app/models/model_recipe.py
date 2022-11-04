# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app import DATABASE
from flask import flash

from flask_app.models import model_user


DATABASE ="recipes_db"
    # model the class after the friend table from our database 
class Recipe:
    def __init__(self , data):
        # ADD attributes for every column in our database table 
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data ['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # C
    @classmethod 
    def create(cls, data:dict) -> int:
        #add all column names and add all values
        query = "INSERT INTO recipes (name, description , instructions,  user_id) VALUES ( %(name)s, %(description)s, %(instructions)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # R
    @classmethod 
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False 
        


    @classmethod 
    def get_all(cls) -> list:
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        if results:
            all_recipes = []
            for dict in results:
                recipe = cls(dict)
                user_data = {
                    'id': dict['users.id'],
                    'created_at': dict['users.created_at'],
                    'updated_at': dict['users.updated_at'],
                    'first_name': dict['first_name'],
                    'last_name': dict['last_name'],
                    'email': dict['email'],
                    'pw': dict['pw'],
                }
                user = model_user.User(user_data)
                recipe.chef = user
                all_recipes.append((recipe))
            return all_recipes
        return []


                

    # U
    @classmethod 
    def update_one(cls, data:dict) -> None:
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s,  user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # D 
    @classmethod 
    def delete_one(cls , data:dict) -> None:
        # ADD COLUMNS = values for every column that you wish to change in to db
        query= "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validator(data:dict) -> bool:
        is_valid = True

        if len(data['name']) < 1:
            flash('field is required' , 'err_recipes_name')
            is_valid = False
        
        if len(data['description']) < 1:
            flash('field is required' , 'err_recipes_description')
            is_valid = False
        
        if len(data['instructions']) < 1:
            flash('field is required' , 'err_recipes_instructions')
            is_valid = False
        
        

        #some code logic here

        return is_valid 
