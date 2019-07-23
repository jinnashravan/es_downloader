"""test resource downloader"""
from es_downloader.query_builder import ESQuery


def test_get_metadata_result():
    # pylint: disable=missing-docstring
    exp_q_res = {
        u'_id': u'aebbf29e-0c59-4c43-bce6-323cd38b5c58',
        u'_index': u'document-labels-production',
        u'_score': None,
        u'_type': u'label',
        u'sort': [288528],
        u'_source': {
            u'Id': u'aebbf29e-0c59-4c43-bce6-323cd38b5c58',
            u'app_version': 0.16,
            u'created_at': u'2017-06-06T03:36:18.539Z',
            u'custom_marks': None,
            u'doc_properties': {u'doc_country': u'FRA',
                                u'doc_side': u'Front',
                                u'doc_type': u'National Identity Card'},
            u'document_id': 2462712,
            u'project_id': 24,
            u'user_id': 280}
    }

    exp_meta = {"_type": "label", "_score": None,
                "_index": "document-labels-production",
                "size": 1}
    es_q = ESQuery('test_client', 'index', 'path')

    metadata = es_q._get_metadata_result(exp_q_res, size=1)
    assert metadata == exp_meta


def test_get_query_results():
    # pylint: disable=missing-docstring
    exp_q_res = [{
        u'_id': u'aebbf29e-0c59-4c43-bce6-323cd38b5c58',
        u'_index': u'document-labels-production',
        u'_score': None,
        u'_type': u'label',
        u'sort': [288528],
        u'_source': {
            u'Id': u'aebbf29e-0c59-4c43-bce6-323cd38b5c58',
            u'app_version': 0.16,
            u'created_at': u'2017-06-06T03:36:18.539Z',
            u'custom_marks': None,
            u'doc_properties': {
                u'doc_country': u'FRA',
                u'doc_side': u'Front',
                u'doc_type': u'National Identity Card'},
            u'document_id': 2462712,
            u'project_id': 24,
            u'user_id': 280}
    }]

    exp_meta = [{
        u'Id': u'aebbf29e-0c59-4c43-bce6-323cd38b5c58',
        u'app_version': 0.16,
        u'created_at': u'2017-06-06T03:36:18.539Z',
        u'custom_marks': None,
        u'doc_properties': {
            u'doc_country': u'FRA',
            u'doc_side': u'Front',
            u'doc_type': u'National Identity Card'},
        u'document_id': 2462712,
        u'project_id': 24,
        u'user_id': 280}]

    es_q = ESQuery('test_client', 'index', 'path')
    metadata = es_q._get_query_results(exp_q_res)
    assert metadata == exp_meta
