import pytest

import jsonconfig

from messages.text import Twilio
from messages._exceptions import MessageSendError


def twilio_test_configured():
    with jsonconfig.Config('messages') as cfg:
        data = cfg.data
        return ('integration_tester' in cfg.data.keys()
            and 'twilio' in data['integration_tester'])


#Skip all tests if not configured
pytestmark = pytest.mark.skipif(not twilio_test_configured(),
    reason='Tester not configured for messages.text.Twilio')


@pytest.fixture()
def get_twilio():
    """Return a valid Twilio object."""
    t = Twilio(from_='+14807716634',
               to='+79216240965',
               body='test text!',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='integration_tester', save=False)
    return t


def test_twilio_normal_execution(get_twilio):
    t = get_twilio
    resp = t.send()

    resp_dict = resp.json()
    assert resp.status_code == 201
    assert resp_dict['from'] == t.from_
    assert resp_dict['to'] == t.to
    assert resp_dict['body'] == t.body
    assert resp_dict['status'] == 'queued'
    assert resp_dict['error_message'] is None
    assert 'media' in resp_dict['subresource_uris']


def test_twilio_with_empty_body(get_twilio):
    t = get_twilio
    t.body = ''
    t.attachments = None

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


def test_twilio_send_from_unavailable_number(get_twilio):
    t = get_twilio
    t.from_ = '+15005550000'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


def test_twilio_send_from_invalid_number(get_twilio):
    t = get_twilio
    t.from_ = '+15005550001'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


def test_twilio_send_from_another_invalid_number(get_twilio):
    t = get_twilio
    t.__dict__['from_'] = '+123'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response



def test_twilio_from_number_that_is_not_owned_by_your_account(get_twilio):
    t = get_twilio
    t.from_ = '+15005550007'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response



def test_twilio_from_full_sms_queue(get_twilio):
    t = get_twilio
    t.from_ = '+15005550008'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


def test_twilio_to_non_mobile_number(get_twilio):
    t = get_twilio
    t.to = '+15005550009'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response



def test_twilio_send_to_invalid_number(get_twilio):
    t = get_twilio
    t.__dict__['to'] = '123'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response



def test_twilio_cant_route_to_number(get_twilio):
    t = get_twilio
    t.to = '+15005550002'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


def test_twilio_invalid_account_sid(get_twilio):
    t = get_twilio
    token = t.__dict__['_auth'][1]
    t.__dict__['_auth'] = ('invalid_sid', token)

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '404 ' in response



def test_twilio_invalid_auth_token(get_twilio):
    t = get_twilio
    sid = t.__dict__['_auth'][0]
    t.__dict__['_auth'] = (sid, 'invalid_token')

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '401' in response

