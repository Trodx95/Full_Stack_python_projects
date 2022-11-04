from flask_app import app 
from flask import render_template, redirect,session,request

from flask_app.models import model_recipe

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    context = {
        'all_recipes': model_recipe.Recipe.get_all(),
    }
    return render_template('dashboard.html' , **context)