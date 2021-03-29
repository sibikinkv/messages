import pathlib

import pytest
import int_setup

from messages.email_ import Email
from messages._exceptions import MessageSendError, InvalidMessageInputError
from smtplib import SMTPRecipientsRefused


pytestmark = pytest.mark.skipif(not int_setup.integration_test_configured('email'),
    reason='Tester not configured for messages.email_.Email')


TESTDIR = pathlib.Path(__file__).absolute().parent.parent.joinpath('data')


@pytest.fixture()
def get_email():
    return Email(
        subject='[Messages] Integration Test',
        body='Conducting Integration Testing',
        profile='integration_tester',
        attachments=str(TESTDIR.joinpath('file2.png')),
        save=False)


def test_email_good(get_email, capsys):
    e = get_email
    e.to = 'kostyan.9632@gmail.com'
    e.send()
    out, err = capsys.readouterr()
    assert "Message sent" in out


def test_email_bad_auth(get_email):
    e = get_email
    e.auth = 'baDp@ssw0rd'

    with pytest.raises(MessageSendError):
        e.send()


def test_email_no_receiver(get_email):
    e = get_email
    with pytest.raises(SMTPRecipientsRefused):
        e.send()


def test_email_empty_body(get_email):
    e = get_email
    e.to = 'kostyan.9632@gmail.com'
    e.body = ''

    e.send()


def test_email_bad_receiver(get_email):
    e = get_email
    e.to = 'kostyan.9632'

    with pytest.raises(InvalidMessageInputError):
        e.send()
