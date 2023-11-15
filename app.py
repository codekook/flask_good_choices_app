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
        if request.form.get('new_chore'):
            newChore = request.form['new_chore']
            new_chore = Chore(newChore)
            status_check = new_chore.get_chore_completed()
            app.logger.debug('New Chore: ' + newChore + ' | Status: ' + str(status_check))

        if request.form.get('rmove_chore'):
            chore_number = request.form['chore_num']
            Chore.chore_list[int(chore_number)].remove_chore()
            current_chores = Chore.chore_list
            #app.logger.debug('Chore Removed Number: ' + str(chore_number) + ' | Chore List: ' + current_chores)
        
        if request.form.get('reset'):
            for i in Chore.chore_list:
                i.set_chore_completed(False)
                status_check = i.get_chore_completed()
                chore_lst = Chore.chore_list 
                app.logger.debug('Chore: ' + i + '| Status: ' + str(status_check))
            return render_template("index.html", chore_lst=chore_lst)

        if request.form.get('status_complete'):
            chore_complete = request.form['chore_complete']
            Chore.chore_list[int(chore_complete)].set_chore_completed(True)
            status_check = Chore.chore_list[int(chore_complete)].get_chore_completed()
            chore_lst = Chore.chore_list
            app.logger.debug('Chore Completed Number: ' + chore_complete + ' | Status: ' + str(status_check))
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
    
    def chore_score(self, status):
        if status == True:
            #return an emoji
            return "\U0001F600"
        else:
            return "\U0001F636"

if __name__ == '__main__':
    app.run(debug=True)