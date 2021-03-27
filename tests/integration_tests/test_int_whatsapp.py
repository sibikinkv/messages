import pytest
import int_setup

from messages.whatsapp import WhatsApp
from messages._exceptions import MessageSendError

# SKIP TESTS IF ENVIRONMENT NOT PREPPED

#Skip all tests if not configured
pytestmark = pytest.mark.skipif(not int_setup.integration_test_configured('whatsapp'),
    reason='Tester not configured for messages.whatsapp.WhatsApp')


# FIXTURES
@pytest.fixture()
def get_whatsapp():
    """Return a valid WhatsApp instance."""
    return WhatsApp(to='+79216240965',
                    from_='+14155238886',
               body='[Messages] integration test',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='integration_tester', save=False)


# TESTS: Send from

def test_whatsapp_normal_execution(get_whatsapp):
    t = get_whatsapp
    resp = t.send()



def test_whatsapp_with_empty_body(get_whatsapp):
    t = get_whatsapp
    t.body = ''
    t.attachments = None

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


def test_whatsapp_send_from_unavailable_number(get_whatsapp):
    t = get_whatsapp
    t.from_ = '+15005550000'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


def test_whatsapp_send_from_invalid_number(get_whatsapp):
    t = get_whatsapp
    t.from_ = '+15005550001'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response
