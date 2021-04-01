import pytest
import int_setup

from messages.whatsapp import WhatsApp
from messages._exceptions import MessageSendError

@pytest.fixture()
def get_whatsapp():
    return WhatsApp(to='+79216240965',
                    from_='+14155238886',
                    body='[Messages] integration test',
                    attachments='https://imgs.xkcd.com/comics/python.png',
                    profile='integration_tester', save=False)


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


def test_whatsapp_send_from_another_invalid_number(get_whatsapp):
    t = get_whatsapp
    t.__dict__['from_'] = '+123'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


def test_whatsapp_from_number_that_is_not_owned_by_your_account(get_whatsapp):
    t = get_whatsapp
    t.from_ = '+15005550007'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


def test_whatsapp_cant_route_to_number(get_whatsapp):
    t = get_whatsapp
    t.to = '+15005550002'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


def test_whatsapp_invalid_account_sid(get_whatsapp):
    t = get_whatsapp
    token = t.__dict__['_auth'][1]
    t.__dict__['_auth'] = ('invalid_sid', token)

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '404 ' in response


def test_whatsapp_invalid_auth_token(get_whatsapp):
    t = get_whatsapp
    sid = t.__dict__['_auth'][0]
    t.__dict__['_auth'] = (sid, 'invalid_token')

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '401' in response
    assert 'Unauthorized' in response
    assert 'Authenticate' in response
