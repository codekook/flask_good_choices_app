from flask import render_template, request, redirect, url_for, flash
from flask_package.models import User
from flask_package import app, db, bcrypt 
from flask_package.forms import RegistrationForm, LoginForm
from flask_package.helpers import Chore, store_feedback
from flask_login import login_user, logout_user, current_user 

@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template("welcome.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for creating an account!")
        return redirect(url_for('login'))
    
    if form.errors:
        flash('Oops, you need to check your form' + str(form.errors))
        app.logger.error('Validation Error\n' + str(form.errors))
    return render_template("register.html", title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Logged in')
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Oops, something went wrong')
    if form.errors:
        flash('Oops, incorrect email or password' + str(form.errors))
        app.logger.error('Validation Error\n' + str(form.errors))
    return render_template("login.html", title="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if request.form.get('new_chore'):
            newChore = request.form['new_chore']
            new_chore = Chore(newChore)
            status_check = new_chore.get_chore_completed()
            app.logger.debug('New Chore: ' + newChore +
                             ' | Status: ' + str(status_check))

        if request.form.get('rmove_chore'):
            chore_number = request.form['chore_num']
            Chore.chore_list[int(chore_number)].remove_chore()
            current_chores = Chore.chore_list
            # app.logger.debug('Chore Removed Number: ' + str(chore_number) + ' | Chore List: ' + current_chores)

        if request.form.get('reset'):
            for i in Chore.chore_list:
                i.set_chore_completed(False)
                status_check = i.get_chore_completed()
                chore_lst = Chore.chore_list
                app.logger.debug(
                    'Chore: ' + i + '| Status: ' + str(status_check))
            return render_template("index.html", chore_lst=chore_lst)

        if request.form.get('status_complete'):
            chore_complete = request.form['chore_complete']
            Chore.chore_list[int(chore_complete)].set_chore_completed(True)
            status_check = Chore.chore_list[int(
                chore_complete)].get_chore_completed()
            chore_lst = Chore.chore_list
            app.logger.debug('Chore Completed Number: ' +
                             chore_complete + ' | Status: ' + str(status_check))
            return render_template("index.html", chore_lst=chore_lst)

    chore_lst = Chore.chore_list
    return render_template("index.html", chore_lst=chore_lst)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        url = request.form['url']
        store_feedback(url)
        app.logger.debug('Feedback: ' + url)
        flash("Your Feedback: " + url)
        return redirect(url_for("index"))
    return render_template("feedback.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
