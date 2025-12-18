"""
    Tests for the ArticleFetcher module
"""
import pytest
import time
from factiva.analytics import OAuthUser, ArticleFetcher, UIArticle
from factiva.analytics.common import config, const

GITHUB_CI = config.load_environment_value('CI', False)
FACTIVA_CLIENTID = config.load_environment_value("FACTIVA_CLIENTID")
FACTIVA_USERNAME = config.load_environment_value("FACTIVA_USERNAME")
FACTIVA_PASSWORD = config.load_environment_value("FACTIVA_PASSWORD")
ARTICLE_ID = 'WSJO000020221229eict000jh'

def _assert_uiarticle_values(uiarticle: UIArticle):
    assert isinstance(uiarticle, UIArticle)
    assert isinstance(uiarticle.an, str)
    assert isinstance(uiarticle.headline, str)
    assert isinstance(uiarticle.source_code, str)
    assert isinstance(uiarticle.source_name, str)
    assert isinstance(uiarticle.metadata, dict)
    assert isinstance(uiarticle.content, dict)
    assert isinstance(uiarticle.included, list)
    assert isinstance(uiarticle.relationships, dict)
    assert uiarticle.an == ARTICLE_ID
    assert 'headline' in uiarticle.content.keys()
    assert uiarticle.source_code == 'WSJO'
    assert uiarticle.source_name == 'The Wall Street Journal Online'


def test_article_fetcher_env_user():
    """"
    Creates the object using the ENV variable and request the article content to the API service
    """
    time.sleep(const.TEST_REQUEST_SPACING_SECONDS)
    ar = ArticleFetcher()
    article = ar.fetch_single_article(ARTICLE_ID)
    _assert_uiarticle_values(article)


def test_article_fetcher_params_user():
    """
    Creates the object using the passed params and request the article content to the API service
    """
    time.sleep(const.TEST_REQUEST_SPACING_SECONDS)
    o = OAuthUser(client_id=FACTIVA_CLIENTID,
                  username=FACTIVA_USERNAME,
                  password=FACTIVA_PASSWORD)
    ar = ArticleFetcher(oauth_user=o)
    article = ar.fetch_single_article(ARTICLE_ID)
    _assert_uiarticle_values(article)

