from flask import Flask, render_template, request, redirect, url_for, flash
import random
from datetime import datetime
from logging import DEBUG

app = Flask(__name__)

app.secret_key = b'/\xeb~\xd7\xca(%\xf7'

app.logger.setLevel(DEBUG)

feedback_list = []

@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        url = request.form['url']
        new_chore = Chore(url)
        #chore_status = chore_score(new_chore.get_chore_completed)
        app.logger.debug('New Chore : ' + url)

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

def chore_score(get_chore_completed):
    if get_chore_completed == True:
        #return an emoji
        return "\U0001F600"
    else:
        return "\U0001F636"

def store_feedback(url):
    feedback_list.append(dict(
        url=url,
        user='chipcorey',
        date= datetime.utcnow()
        ))

def all_chores_completed(chore_list):
    affirmations = ["Great job!", 
                    "Keep it up!", 
                    "Awesome!", 
                    "Thank you for your hard work!", 
                    "I appreciate you!", 
                    "I'm grateful for you!",
                    "That's kind of you!",
                    "Your help means a lot!",
                    "It means the world to me!"
                    ]

    for i in chore_list:
        if i.get_chore_completed() == True:
            return random.choice(affirmations)

def reset_chore_list(chore_list):
    for i in chore_list:
        i.set_chore_completed(False)
        print(chore_score(i.get_chore_completed()))

class Chore(object):

    chore_list = []
    frequency_list = ["Daily", "Weekly", "Monthly"]

    def __init__(self, chore):
        self.__chore = chore
        self.__completed = False
        self.__frequency = "Daily"
        self.chore_list.append(self)

    def __repr__(self):
        return self.__chore

    def set_chore(self, chore):
        self.__chore = chore 

    def get_chore(self):
        return self.__chore 

    def remove_chore(self):
        return Chore.chore_list.remove(self)
    
    def set_chore_completed(self, completed):
        self.__completed = completed
    
    def get_chore_completed(self):
        return self.__completed
    
    def set_frequency(self, frequency):
        self.__frequency = frequency 
    
    def get_frequency(self):
        return self.__frequency

if __name__ == '__main__':
    app.run(debug=True)