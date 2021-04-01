import pytest
import int_setup

from messages._exceptions import MessageSendError
from messages.telegram import TelegramBot



pytestmark = pytest.mark.skipif(not int_setup.integration_test_configured('telegrambot'),
    reason='Tester not configured for messages.telegram.TelegramBot')


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


def test_telegram_send_good(get_telegram):
    t = get_telegram
    t.send()


def test_telegram_with_empty_body(get_telegram):
    t = get_telegram
    t.body = ''
    t.send()


def test_telegram_with_empty_subject(get_telegram):
    t = get_telegram
    t.subject = ''
    t.send()


def test_telegram_with_attachment(get_telegram):
    t = get_telegram
    t.attachments = 'https://cutt.ly/zx0ClAH'
    t.send()


def test_telegram_with_attachment_and_empty_body(get_telegram):
    t = get_telegram
    t.body = ''
    t.attachments = 'https://cutt.ly/zx0ClAH'
    t.send()


def test_telegram_send_bad_credentials(get_telegram):
    t = get_telegram
    t._auth = 'BadCredentials'
    t.base_url = "https://api.telegram.org/bot" + t._auth
    with pytest.raises(MessageSendError):
        t.send()
