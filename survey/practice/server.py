from flask import Flask, render_template ,redirect , request , session
app = Flask(__name__)
app.secret_key ="mykey"

#display route
@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/users', methods=['POST'])
def create_user():
    print("Got Post Info")
    print(request.form)
    session['name'] = request.form['name']
    session['location'] = request.form['Location']
    session['language'] = request.form['language']
    session['comment'] = request.form['comment']
    return redirect("/show")	



@app.route("/show")
def show_user():
    print("Showing the User Info From the Form")
    print(request.form)
    return render_template("tracking.html")


# action route
# @app.route('/tracking.html', methods=['POST'])
# def form():
    
#     return render_template('/index.html')
#     return redirect('/tracking.html')


# @app.route('/', methods=["POST", "GET"])
# def index():
#     if request.method == "POST":
#         req = request.form
#         input = req["usr_input"]
#         return input
#     else :
#         return render_template('index.html')

    # credit_card_number = request.form['credit_card_number']
    
    # session is a dictionary 
    # session['ccn'] = (request.form['credit_card_number'])[-4:]

    # this is what you want to do 

#display route



#this must be on the bottom of this file
if __name__=="__main__":
    app.run(debug=True)