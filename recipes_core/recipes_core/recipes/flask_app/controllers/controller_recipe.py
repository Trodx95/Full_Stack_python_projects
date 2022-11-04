from flask_app import app, bcrypt
from  flask import render_template, redirect , request , session

    # this imports the model file
from flask_app.models import model_recipe

    # Display route
@app.route('/recipe/new')
def recipe_new():
    return render_template('recipe_new.html')

    # ACTION ROUTE
@app.route('/recipe/create', methods=['POST'])
def recipe_create():
    #validations 
    if not model_recipe.Recipe.validator(request.form):
        return redirect('/recipe/new')
    # create recipe 
    data = {
        **request.form,
        'user_id' : session['uuid']
    }
    model_recipe.Recipe.create(data)
    return redirect('/')

    # Display route
@app.route('/recipe/<int:id>')
def recipe_show(id):
    context = {
        'recipe' : model_recipe.Recipe.get_one({'id' : id}),
        
        
    }
    return render_template('recipe_show.html', **context)
    
    # Display route
@app.route('/recipe/<int:id>/update')
def recipe_edit(id):
    context = {
        'recipe' : model_recipe.Recipe.get_one({'id' : id})
    }
    return render_template('recipe_edit.html', **context)

    # ACTION ROUTE
@app.route('/recipe/<int:id>/update', methods=['POST'])
def recipe_update(id):
    #validations 
    if not model_recipe.Recipe.validator(request.form):
        return redirect(f'/recipe/{id}/edit')
    data = {
        **request.form,
        'user_id': session['uuid'],
        'id': id
    }
    
    model_recipe.Recipe.update_one(data)
    
    return redirect('/')

@app.route('/recipe/<int:id>/delete')
def recipe_delete(id):
    model_recipe.Recipe.delete_one({'id' : id})
    return redirect('/')

