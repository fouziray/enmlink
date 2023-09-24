from __future__ import absolute_import
import logging
from responses import activate as mock_responses
from nose import (with_setup)
from nose.tools import (assert_raises)
import enmscripting
from enmscripting.private.session import (ExternalSession, _AUTH_COOKIE_KEY)
from enmscripting.security.authenticator import (is_password_change_redirect,
                                                 UsernameAndPassword, SsoToken, _AUTH_COOKIE_KEY)
from enmscripting.enmsession import (UnauthenticatedEnmSession)
from .session_mock_utils import *
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

logging.basicConfig()
logging.getLogger().setLevel(level=logging.DEBUG)


def mock_open(read_data=''):
    file_handler = MagicMock()
    file_handler.__enter__ = MagicMock(return_value=file_handler)
    file_handler.readline = MagicMock(return_value=read_data)
    open_function = MagicMock(return_value=file_handler)
    return open_function


@mock_responses
@with_setup(setup_session_mock, teardown_session_mock)
def test_open():
    mock_success_login_response('testCookie')
    session = enmscripting.open(login_url, 'username', 'pass')._session

    assert session
    assert isinstance(session, ExternalSession)


@mock_responses
@with_setup(setup_session_mock, teardown_session_mock)
def test_open_with_username_and_password_authenticator():
    mock_success_login_response('testCookie')
    not_authenticated_session = enmscripting.open(login_url)

    assert not_authenticated_session
    assert isinstance(not_authenticated_session, UnauthenticatedEnmSession)

    session = not_authenticated_session.with_credentials(UsernameAndPassword('username', 'pass'))._session

    assert session
    assert isinstance(session, ExternalSession)


@patch('io.open', mock_open(read_data="the-saved-token-value"))
def test_open_with_ssotoken_authenticator():
    not_authenticated_session = enmscripting.open(login_url)

    assert not_authenticated_session
    assert isinstance(not_authenticated_session, UnauthenticatedEnmSession)

    session = not_authenticated_session.with_credentials(SsoToken.from_file('token/file/path'))._session

    assert session
    assert isinstance(session, ExternalSession)
    assert session.cookies[_AUTH_COOKIE_KEY] == "the-saved-token-value"
    assert session.authenticator().token() == "the-saved-token-value"


@mock_responses
@with_setup(setup_session_mock, teardown_session_mock)
def test_open_authentication_failed_auth_code_not_0():
    mock_failed_login_response('testCookie')
    assert_raises(ValueError, enmscripting.open, login_url, 'username', 'pass')


@mock_responses
@with_setup(setup_session_mock, teardown_session_mock)
def test_open_no_cookie():
    mock_success_login_response(None)
    assert_raises(ValueError, enmscripting.open, login_url, 'username', 'pass')


@mock_responses
@with_setup(setup_session_mock, teardown_session_mock)
def test_close():

    mock_success_login_response()
    enm_session = enmscripting.open(login_url, 'username', 'pass')

    session = enm_session._session
    assert len(session.cookies) is 1

    mock_logout_response()
    enmscripting.close(enm_session)
    assert len(session.cookies) is 0


@mock_responses
@with_setup(setup_session_mock, teardown_session_mock)
def test_open_password_reset_required():
    mock_failed_login_response('testCookie', True)
    try:
        enmscripting.open(login_url, 'username', 'pass')
        assert False, 'Open should throw ValueError, when user is required to change password'
    except ValueError as e:
        assert 'password change required' in str(e), 'Incorrect error message [%s]' % str(e)


def test_login_response_redirect_true():
    assert is_password_change_redirect('{"code":"PASSWORD_RESET","message":"Password must be reset."}') is True


def test_login_response_redirect_false():
    assert is_password_change_redirect('any other content') is False
