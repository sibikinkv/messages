import pytest

from messages._exceptions import MessageSendError
from messages.telegram import TelegramBot


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


def test_telegram_with_empty_body(get_twilio):
    t = get_telegram
    t.body = ''
    t.send()


def test_telegram_with_empty_subject(get_twilio):
    t = get_telegram
    t.subject = ''
    t.send()


def test_telegram_with_attachment_and_empty_body(get_twilio):
    t = get_telegram
    t.body = ''
    t.attachments = 'https://sun9-26.userapi.com/impf/QfKkHYUE8b1ZLb-7RPgrBqZlhNiBM5Sv9DLpAA/CoC8rWCVHlw.jpg?size=800x800&quality=96&sign=b26802ca7be47a62a27e009247e55a42&type=album'
    t.send()


def test_telegram_send_bad_credentials(get_telegram):
    t = get_telegram
    t._auth = 'BadCredentials'
    t.base_url = "https://api.telegram.org/bot" + t._auth
    with pytest.raises(MessageSendError):
        t.send()
