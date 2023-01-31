from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User



@app.route('/user/edit/<int:id>')
def edit_users(id):
    if 'users_id' not in session:
        return redirect('/')
    else:
        userdata = {
            'id': session['users_id']
        }
    theUser = User.get_user_by_id(userdata)
    data = {
        "id": id
    }
    return render_template('edit_user.html', user = theUser, oneUser = User.get_user_by_id(data))

@app.route('/updateUser', methods=['POST'])
def updateUser():
    isValid = User.validate_paint(request.form)
    if not isValid:
        return redirect(f'/user/edit/{request.form["id"]}')
    User.update(request.form)
    return redirect('/')


@app.route('/user/delete/<int:id>')
def deleteUser(id):
    data = {
        "id": id
    }
    User.delete_user(data)
    return redirect('/')