from flask_app import app
    # remeber to continually add controller files as you create them. 
from flask_app.controllers import controller_user, controller_routes, controller_show

    # this needs to be at the bottom 
if __name__=="__main__":
    app.run(debug=True)
