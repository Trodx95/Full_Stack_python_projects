from flask_app import app, bcrypt
from flask import render_template, redirect, request, session

# this imports the model file
from flask_app.models import model_show, model_user

# Display route


@app.route('/show/new')
def show_new():
    return render_template('show_new.html')

    # ACTION ROUTE


@app.route('/show/create', methods=['POST'])
def show_create():
    # validations
    if not model_show.Show.validator(request.form):
        return redirect('/show/new')
    # create show
    data = {
        **request.form,
        'user_id': session['uuid']
    }
    model_show.Show.create(data)
    return redirect('/')

    # Display route


@app.route('/show/<int:id>/show')
def show_show(id):
    context = {
        'show': model_show.Show.get_one_by_id({'id': id}),
        'user': model_user.User.get_one({'id': session['uuid']})

    }
    return render_template('show_show.html', **context)

    # Display route


@app.route('/show/<int:id>/edit')
def show_edit(id):
    context = {
        'show': model_show.Show.get_one({'id': id})
    }
    return render_template('show_edit.html', **context)

    # ACTION ROUTE


@app.route('/show/<int:id>/edit', methods=['POST'])
def show_update(id):
    # validations
    if not model_show.Show.validator(request.form):
        return redirect(f'/show/{id}/edit')
    data = {
        **request.form,
        'id': id
    }
    show = model_show.Show.update_one(data)

    return redirect('/')


@app.route('/show/<int:id>/delete')
def show_delete(id):
    model_show.Show.delete_one({'id': id})
    return redirect('/')
