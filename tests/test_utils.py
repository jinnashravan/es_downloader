import os
import pytest

from es_downloader.config import get_media_provider_url
from es_downloader.utils import find_item_dict


# @pytest.mark.parametrize("dotted_key,exp_res", [
#     ('test1', 1),
#     ('test3.test31', {'test32': [4]}),
#     ('test3.test31.test32', [4]),
#     ('test3.test31.test32', [4]),
#     ('test3.test31.test', [{'test': 324}]),
# ])
# def test_get_url_template_doc_prod(dotted_key, exp_res):
#     # pylint: disable=missing-docstring
#     orig_dic = {'test1': 1, 'test2': {1: 2}, 'test3': {'test31': {'test32': [4]}}, 'test4': [{'id': 5}]}
#
#     assert exp_res == find_item_dict(orig_dic, dotted_key)


def test_find_item_dict():
    # pylint: disable=missing-docstring
    orig_dic = {'test1': 1, 'test2': {1: 2}, 'test3': {'test31': {'test32': [4]}}, 'test4': [{'id': 5}]}
    dotted_path = None
    key = 'test1'

    assert orig_dic, key == find_item_dict(orig_dic, dotted_path, key)


def test_find_item_dict1():
    # pylint: disable=missing-docstring
    orig_dic = {'test1': 1, 'test2': {1: 2}, 'test3': {'test31': {'test32': [4]}}, 'test4': [{'id': 5}]}
    dotted_path = 'test3.test31'
    key = 'test32'

    assert {'test32': [4]}, 'test32' == find_item_dict(orig_dic, dotted_path, key)


def test_find_item_dict1():
    # pylint: disable=missing-docstring
    orig_dic = {'test1': 1, 'test2': {1: 2}, 'test3': {'test31': {'test32': [4]}}, 'test4': [{'id': 5}]}
    dotted_path = 'test4'
    key = 'id'

    assert [{'id': 5}], 'id' == find_item_dict(orig_dic, dotted_path, key)


def test_get_media_provider_url_silo():
    os.environ['MEDIA_PROVIDER_SERVICE_HOST'] = '10.10.1.0'
    os.environ['MEDIA_PROVIDER_SERVICE_PORT'] = '80'

    exp = 'http://10.10.1.0:80/silo'
    assert get_media_provider_url() == exp


def test_get_media_provider_url():
    assert get_media_provider_url() == 'https://media-provider.eu-west-1.citrix.onfido.xyz/silo'
