from flask import Flask 
app = Flask(__name__)
app.secret_key ="12931812-xasx22-123sd-22"
# DATABASE = 'recipes_db'

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)