"""utility functions"""
import copy
import json

import boto3
import os
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from es_downloader.config import DEFAULT_AWS_REGION


def create_es_client(host, aws_profile=None, port=443,
                     region=DEFAULT_AWS_REGION):
    """create elasticsearch client

    :param host: host name
    :param port: port number
    :param aws_profile: aws profile
    :param region: aws region name
    :return: es client
    """
    if aws_profile is None:
        session = boto3.session.Session(region_name=region)
    else:
        session = boto3.session.Session(profile_name=aws_profile,
                                        region_name=region)

    credentials = session.get_credentials()
    awsauth = AWS4Auth(credentials.access_key,
                       credentials.secret_key,
                       region,
                       'es',
                       session_token=credentials.token)

    es_client = Elasticsearch(
        hosts=[{'host': host, 'port': port}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=120)

    return es_client


def write_file(file_path, records):
    """write list of items in file line by line
    :param file_path: path to local file
    :param records: list of records
    """
    if not isinstance(records, list):
        records = [records]

    with open(file_path, 'w') as res_f:
        for record in records:
            res_f.write(json.dumps(record) + '\n')


def load_ids_file(path):
    with open(path, 'r') as f:
        ids = [a.strip() for a in f if a.strip()]

    return ids


def find_item_dict(dictionary, dotted_path, key):
    dic_cp = copy.deepcopy(dictionary)
    if dotted_path is None:
        dotted_keys = []
    else:
        dotted_keys = dotted_path.split('.')

    while dotted_keys:
        k = dotted_keys.pop(0)
        dic_cp = dic_cp[k]
    return dic_cp, key
