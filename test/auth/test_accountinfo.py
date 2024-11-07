"""
    Tests for the AccountInfo module
"""
import pytest
import time
from factiva.analytics import AccountInfo
from factiva.analytics.common import config, const

GITHUB_CI = config.load_environment_value('CI', False)
FACTIVA_USERKEY = config.load_environment_value("FACTIVA_USERKEY")
DUMMY_KEY = 'abcd1234abcd1234abcd1234abcd1234'


def _test_userkey_types(usr):
    """"
    Checks the correct types were returned.
    """
    if isinstance(usr, str):
        usr = AccountInfo(stats=True)
    assert isinstance(usr.user_key.key, str)
    assert isinstance(usr.user_key.cloud_token, dict)
    assert isinstance(usr.account_name, str)
    assert isinstance(usr.active_product, str)
    # assert isinstance(usr.max_allowed_concurrent_extractions, int)
    assert isinstance(usr.max_allowed_extracted_documents, int)
    assert isinstance(usr.max_allowed_extractions, int)
    assert isinstance(usr.remaining_documents, int)
    assert isinstance(usr.remaining_extractions, int)
    # assert isinstance(usr.total_downloaded_bytes, int or str)
    assert isinstance(usr.total_extracted_documents, int)
    assert isinstance(usr.total_extractions, int)
    assert isinstance(usr.total_stream_instances, int)
    assert isinstance(usr.total_stream_subscriptions, int)
    assert isinstance(usr.enabled_company_identifiers, list)
    # Assert streams
    # Assert extractions


def _test_userkey_values(usr):
    """
    Checks if values within the expected lengths and ranges
    were returned
    """
    if isinstance(usr, str):
        usr = AccountInfo(stats=True)
    assert usr.user_key.key == FACTIVA_USERKEY
    assert len(usr.account_name) >= 0
    assert len(usr.active_product) >= 0
    # assert usr.max_allowed_concurrent_extractions >= 0
    assert usr.max_allowed_extracted_documents >= 0
    assert usr.max_allowed_extractions >= 0
    # assert usr.total_downloaded_bytes >= 0
    assert usr.total_extracted_documents >= 0
    assert usr.total_extractions >= 0
    assert usr.total_stream_instances >= 0
    assert usr.total_stream_subscriptions >= 0
    assert len(usr.enabled_company_identifiers) >= 0

def test_invalid_key():
    """
    Creates an object from the provided string and request the usage details to the API service
    The key is invalid and this should validate how the error is processed
    """
    time.sleep(const.TEST_REQUEST_SPACING_SECONDS)
    with pytest.raises(ValueError, match=r'Factiva User-Key does not exist or inactive.'):
        AccountInfo(DUMMY_KEY)


def test_invald_lenght_key():
    """
    Attempts to create an object with malformed keys. This requires assert the raised exception.
    """
    with pytest.raises(ValueError, match=r'Factiva User-Key has the wrong length'):
        AccountInfo('abc')

def test_userkey_with_stats():
    """"
    Creates the object using the ENV variable and request the usage details to the API service
    """
    time.sleep(const.TEST_REQUEST_SPACING_SECONDS)
    usr = AccountInfo()
    _test_userkey_types(usr)
    _test_userkey_values(usr)


def test_user_with_parameter_and_stats():
    """
    API Key is passed as a string
    """
    time.sleep(const.TEST_REQUEST_SPACING_SECONDS)
    usr = AccountInfo(FACTIVA_USERKEY)
    _test_userkey_types(usr)
    _test_userkey_values(usr)
