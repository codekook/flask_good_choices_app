"""Routes controls the application, executing all website functionality submitted by the user."""

from flask import render_template, request, redirect, url_for, flash
from flask_package.models import User, Chore
from flask_package import app, db, bcrypt
from flask_package.forms import RegistrationForm, LoginForm
from flask_package.helpers import store_feedback, all_chores_completed, generate_happy_emoji
from flask_login import login_user, logout_user, current_user
from datetime import date

@app.route("/")
@app.route('/welcome', methods=["GET", "POST"])
def welcome():

    """Renders the welcome page and registration."""

    return render_template("welcome.html")

@app.route('/register', methods=['GET', 'POST'])
def register():

    """Registers new users and redirects them to the login page."""

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        today = date.today()
        user = User(date=today,
                    username=form.username.data,
                    email=form.email.data,
                    password=hashed_password
                    )
        db.session.add(user)
        db.session.commit()
        flash("Thanks for creating an account!")
        return redirect(url_for('login'))

    if form.errors:
        flash('Oops, you need to check your form' + str(form.errors))
        app.logger.error('Validation Error\n' + str(form.errors))
    
    return render_template("register.html", title='Register', form=form)

@app.route('/register_partial', methods=['GET', 'POST'])
def register_partial():

    """Returns the HTMX partial for the registration page.  Not yet in use."""

    return render_template("register_partial.html")

@app.route('/cancel_register_partial', methods=['GET'])
def cancel_register_partial():

    """Cancels the HTMX partial for the registration page.  Not yet in use."""

    return render_template("cancel_register_partial.html")

@app.route('/login', methods=['GET', 'POST'])
def login():

    """Renders the login page and validates user login credentials."""

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

    """Logs a user out and redirects the user to the welcome page."""

    logout_user()
    return redirect(url_for('welcome'))

@app.route('/index', methods=['GET', 'POST'])
def index():

    """Renders the main page for creating, deleting, and managing chores."""

    if current_user.is_authenticated:
        print("current_user: ", current_user.username)
        if request.method == "POST":
            if request.form.get('new_chore'):
                chore_input = request.form['new_chore']
                new_chore = Chore(
                chore=chore_input, frequency='Weekly', completed='\U0001F636', username=current_user.username)
                db.session.add(new_chore)
                db.session.commit()
                app.logger.debug('New Chore: ' + chore_input)

            if request.form.get('rmove_chore'):
                chore_number = request.form['chore_num']
                chore_to_delete = db.delete(Chore).where(Chore.chore_id == chore_number)
                db.session.execute(chore_to_delete)
                db.session.commit()
                app.logger.debug('Deleted Chore: ' + str(chore_to_delete))

            if request.form.get('reset'):
                reset_chores = db.update(Chore).values(completed="\U0001F636")
                db.session.execute(reset_chores)
                db.session.commit()
                app.logger.debug('Reset Chores')

            if request.form.get('completed'):
                chore_number = request.form['chore_num']
                happy_emoji = generate_happy_emoji()
                chore_completed = db.update(Chore).where(
                    Chore.chore_id == chore_number).values(completed=happy_emoji)
                db.session.execute(chore_completed)
                db.session.commit()
                app.logger.debug('Chore Completed Number: ' + str(chore_completed))

        chore_table_info = db.session.execute(db.select(Chore.chore_id,
                                                        Chore.chore, Chore.completed).where(Chore.username == current_user.username).order_by(Chore.chore_id)).fetchall()
        app.logger.debug('Chore table info: ' + str(chore_table_info))
        affirm = all_chores_completed(chore_table_info)
        app.logger.debug('All Chores Completed: ' + str(affirm))
        if affirm is not None:
            flash(affirm)

        return render_template("index.html", chore_lst=chore_table_info)
    else:
        return redirect(url_for('welcome'))

@app.route('/add_chore_partial', methods=['GET'])
def add_chore_partial():

    '''Returns the HTMX partial for the add chore form.'''

    return render_template("add_chore_partial.html")

@app.route('/cancel_add_chore_partial', methods=['GET'])
def cancel_add_chore_partial():

    '''Cancels the HTMX partial for the add chore form.'''

    return render_template("cancel_add_chore_partial.html")

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():

    """Renders the feedback page."""

    if current_user.is_authenticated:
        if request.method == "POST":
            url = request.form['url']
            store_feedback(url)
            app.logger.debug('Feedback: ' + url)
            flash("Your Feedback: " + url)
            return redirect(url_for("index"))
        return render_template("feedback.html")
    else:
        return redirect(url_for('welcome'))

@app.errorhandler(404)
def page_not_found(e):

    """Renders Page Not Found 404 Error."""

    return render_template("404.html"), 404
