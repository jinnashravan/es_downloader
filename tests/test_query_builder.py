"""test query builder"""
import os
import pytest
from doubles import allow
from elasticsearch import helpers

from es_downloader.config import DOWNLOAD_TYPE_DOC, \
    DOWNLOAD_TYPE_LIVE_IMG, DOWNLOAD_TYPE_LIVE_VID
from es_downloader.exception import ElasticSearchDownloader, \
    NoResultsException
from es_downloader.main import _load_query
from es_downloader.query_builder import ESQuery
from es_downloader.url_builder import UrlBuilder


def test_get_url_template_doc_prod():
    # pylint: disable=missing-docstring
    exp_url = "https://imago.onfido.com/api/documents/{id}/download"

    es_q = UrlBuilder(index='index', download_type=DOWNLOAD_TYPE_DOC)
    url = es_q._get_url_template()
    assert url == exp_url


def test_get_url_template_liveimg_prod():
    # pylint: disable=missing-docstring
    exp_url = "https://imago.onfido.com/api/live_photos/{id}/download"

    es_q = UrlBuilder(index='index', download_type=DOWNLOAD_TYPE_LIVE_IMG)
    url = es_q._get_url_template()
    assert url == exp_url


def test_get_url_template_livevid_prod():
    # pylint: disable=missing-docstring
    exp_url = "https://imago.onfido.com/api/live_videos/{id}/download"

    es_q = UrlBuilder(index='index', download_type=DOWNLOAD_TYPE_LIVE_VID)
    url = es_q._get_url_template()

    assert url == exp_url


def test_get_url_template_doc_dev():
    # pylint: disable=missing-docstring
    exp_url = "https://imago-dev.onfido.com/api/documents/{id}/download"

    es_q = UrlBuilder(index='index', download_type=DOWNLOAD_TYPE_DOC, imago_dev=True)
    url = es_q._get_url_template()
    assert url == exp_url


def test_get_url_template_liveimg_dev():
    # pylint: disable=missing-docstring
    exp_url = "https://imago-dev.onfido.com/api/live_photos/{id}/download"

    es_q = UrlBuilder(index='index', download_type=DOWNLOAD_TYPE_LIVE_IMG, imago_dev=True)
    url = es_q._get_url_template()
    assert url == exp_url


def test_get_url_template_livevid_dev():
    # pylint: disable=missing-docstring
    exp_url = "https://imago-dev.onfido.com/api/live_videos/{id}/download"

    es_q = UrlBuilder(index='index', download_type=DOWNLOAD_TYPE_LIVE_VID, imago_dev=True)
    url = es_q._get_url_template()

    assert url == exp_url


def test_get_url_template_doc_prod_metadata():
    # pylint: disable=missing-docstring
    exp_url = "https://imago.onfido.com/api/documents/{id}"

    es_q = UrlBuilder(index='index', download_type=DOWNLOAD_TYPE_DOC, metadata_url=True)
    url = es_q._get_url_template()
    assert url == exp_url


def test_get_url_template_liveimg_prod_metadata():
    # pylint: disable=missing-docstring
    exp_url = "https://imago.onfido.com/api/live_photos/{id}"

    es_q = UrlBuilder(index='index', download_type=DOWNLOAD_TYPE_LIVE_IMG, metadata_url=True)
    url = es_q._get_url_template()
    assert url == exp_url


def test_get_url_template_livevid_prod_metadata():
    # pylint: disable=missing-docstring
    exp_url = "https://imago.onfido.com/api/live_videos/{id}"

    es_q = UrlBuilder(index='index', download_type=DOWNLOAD_TYPE_LIVE_VID, metadata_url=True)
    url = es_q._get_url_template()

    assert url == exp_url


def test_raises_notexists():
    # pylint: disable=missing-docstring
    with pytest.raises(ElasticSearchDownloader):
        _load_query('some/random/path')


def test_raises():
    # pylint: disable=missing-docstring
    current_folder = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_folder, 'query_results.json')

    with pytest.raises(ElasticSearchDownloader):
        _load_query(path)


def test_query_es_no_results():
    # pylint: disable=missing-docstring
    def generator(list_vals):
        # pylint: disable=missing-docstring
        for a in list_vals:
            yield a

    es = ESQuery('es_client', 'index', 'query')
    allow(helpers).scan.and_return(generator([]))

    try:
        es._query_es()
    except NoResultsException:
        pass
    else:
        raise AssertionError('Expected test to raise NoResultsException.')


def test_query_es_size():
    # pylint: disable=missing-docstring
    def generator(list_vals):
        for a in list_vals:
            yield a

    es = ESQuery('es_client', 'index', 'query', size=2)
    allow(helpers).scan.and_return(list(generator([0, 1, 2])))

    res = es._query_es()

    assert res == [0, 1]


def test_get_url_template_doc_media_provider():
    # pylint: disable=missing-docstring
    exp_url = "https://media-provider.eu-west-1.citrix.onfido.xyz/silo/documents/{id}/download"

    es_q = UrlBuilder(index='index', download_type=DOWNLOAD_TYPE_DOC, media_provider=True)
    url = es_q._get_url_template()
    assert url == exp_url
