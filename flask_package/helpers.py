import random
from datetime import datetime

feedback_list = []

def store_feedback(url):
    feedback_list.append(dict(
        url=url,
        user='chipcorey',
        date=datetime.utcnow()
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

def emoji_status():
    return "\U0001F636"

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
            # return an emoji
            return "\U0001F600"
        else:
            return "\U0001F636"
