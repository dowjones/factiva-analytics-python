"""
    Tests for the UserKey module
"""
import pytest
import time
from factiva.analytics import UserKey
from factiva.analytics.common import config, const

GITHUB_CI = config.load_environment_value('CI', False)
FACTIVA_USERKEY = config.load_environment_value("FACTIVA_USERKEY")
DUMMY_KEY = 'abcd1234abcd1234abcd1234abcd1234'


def test_userkey_from_env():
    """
    Creates an empty object from the ENV variable with a value only for the key property
    """
    time.sleep(const.TEST_REQUEST_SPACING_SECONDS)
    usr = UserKey()
    assert usr.key == FACTIVA_USERKEY
    assert isinstance(usr.cloud_token, dict)


def test_user_with_parameter_and_stats():
    """
    API Key is passed as a string and stats=True
    """
    time.sleep(const.TEST_REQUEST_SPACING_SECONDS)
    usr = UserKey(FACTIVA_USERKEY)
    assert usr.key == FACTIVA_USERKEY
    assert isinstance(usr.cloud_token, dict)


def test_invalid_key():
    """
    Creates an object from the provided string and request the usage details to the API service
    The key is invalid and this should validate how the error is processed
    """
    time.sleep(const.TEST_REQUEST_SPACING_SECONDS)
    with pytest.raises(ValueError, match=r'Factiva User-Key does not exist or inactive.'):
        UserKey(DUMMY_KEY)


def test_invald_lenght_key():
    """
    Attempts to create an object with malformed keys. This requires assert the raised exception.
    """
    with pytest.raises(ValueError, match=r'Factiva User-Key has the wrong length'):
        UserKey('abc')
