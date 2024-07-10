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
    if "\U0001F636" not in emo_list and len(emo_list) > 0:
        return random.choice(affirmations)
    else:
        return None 
    
def generate_happy_emoji():

    """Returns a random emoji face when a chore is completed"""

    emojis_list = [
        "\U0001F600",
        "\U0001F642",
        "\U0001F60A",
        "\U0001F917",
        "\U0001F973",
        "\U0001F60E",
        "\U0001F60B"
    ]

    return random.choice(emojis_list)
