import pytest
from flask_package import helpers
from flask_package.models import Feedback
from flask_package import db

@pytest.mark.parametrize('feedback_text', ['Great site'])
def test_store_feedback(test_app, feedback_text):

    '''Test if the feedback submitted by a user is stored in the database'''

    with test_app.app_context():
        # Store feedback with user_id=1 (assuming a test user exists)
        helpers.store_feedback(feedback_text, user_id=1)

        # Query the database to verify it was saved
        saved_feedback = db.session.query(Feedback).filter_by(
            feedback_text=feedback_text).first()

        assert saved_feedback is not None
        assert saved_feedback.feedback_text == feedback_text
        assert saved_feedback.user_id == 1

        # Cleanup - delete the test feedback
        db.session.delete(saved_feedback)
        db.session.commit()

def test_all_chores_completed(affirmations_list, chore_table_info):

    '''Tests if the all_chores_completed function returns an affirmation from the affirmation list'''

    result = helpers.all_chores_completed(chore_table_info)
    assert result

@pytest.mark.parametrize("emojis_list", [[
    "\U0001F600",
    "\U0001F642",
    "\U0001F60A",
    "\U0001F917",
    "\U0001F973",
    "\U0001F60E",
    "\U0001F60B"
]])
def test_generate_happy_emoji(emojis_list):
    result = helpers.generate_happy_emoji()
    assert result in emojis_list