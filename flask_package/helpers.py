"""Helpers has two functions that assist in the functionality of the application."""

import random
from datetime import datetime

feedback_list = []

def store_feedback(url):

    """Appends the user feedback dictionary to the feedback list"""

    feedback_list.append(dict(
        url=url,
        user='chipcorey',
        date=datetime.utcnow()
    ))

def all_chores_completed(chore_table_info):

    """Returns an affirmation when all chores are completed"""

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

    emo_list = []
    for i, j, k in chore_table_info:
        emo_list.append(k)
    if all(j == "\U0001F600" for j in emo_list):
        return random.choice(affirmations)
