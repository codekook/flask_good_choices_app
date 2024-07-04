import pytest
from flask_package import helpers

@pytest.mark.parametrize('url', ['Great site'])
def test_store_feedback(url):

    '''Test if the feedback submitted by a user will be added to the feedback list'''

    helpers.store_feedback(url)
    result = helpers.feedback_list[0]['url']
    assert result == helpers.feedback_list[0]['url']

@pytest.mark.parametrize("chore_table_info", [
        [(25, 'Clean Room', '\U0001F642'), (15, 'Wipe Table', '\U0001F973')],
        [(37, 'Empty trash', '\U0001F600')]
        ])
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