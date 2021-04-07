import pathlib

import pytest
import int_setup

from messages.email_ import Email
from messages.telegram import TelegramBot
from messages._exceptions import MessageSendError, InvalidMessageInputError

from unittest.mock import patch


pytestmark = pytest.mark.skipif(not int_setup.integration_test_configured('email'),
    reason='Tester not configured for messages.email_.Email')


TESTDIR = pathlib.Path(__file__).absolute().parent.parent.joinpath('data')

@pytest.fixture()
def get_email():
    return Email(
        subject='[Messages] Integration Test',
        body='Conducting Integration Testing',
        profile='integration_tester',
        save=False)

@pytest.fixture()
def get_telegram():
    return TelegramBot(
        chat_id='344851599',
        profile='integration_tester',
        from_='Integration Tester',
        subject='[Messages] Integration Testing',
        body='Conducting Integration Testing',
        save=False
    )


@patch("messages.email_.Email.send")
@patch("messages.telegram.TelegramBot.send")
def test_sys_volume(mock_email_send, mock_telegram_send ,get_email, capsys, get_telegram):
    e = get_email
    t = get_telegram

    tries = 10
    succ = 0
    for _ in range(tries):
        e.to = 'kostyan.9632@gmail.com'
        e.send()
        out, err = capsys.readouterr()

        #if "Message sent" in out:
        succ += 1

        try:
            t.send()
        except MessageSendError as e:
            succ -= 1

    assert succ == tries
    assert mock_email_send.called
    assert mock_telegram_send.called
