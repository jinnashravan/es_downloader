"""es_downloader main entry point"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from datetime import datetime
import os
import json

from os.path import join, exists

from es_downloader.config import HOST, DEFAULT_AWS_REGION, \
    QUERY_RESULTS_FILE, METADATA_RESULTS_FILE
from es_downloader.exception import ElasticSearchDownloader
from es_downloader.file_downloader import download_files
from es_downloader.metadata_logger import write_meta_result_es, write_log_paths
from es_downloader.query_builder import ESQuery
from es_downloader.url_builder import UrlBuilder
from es_downloader.utils import create_es_client, write_file, load_ids_file


def _create_parser():
    """A function to create the argument parser to parse the user's input.

    :return: The argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Command line tool for downloading data "
                    "from Elastic search clusters")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-qp', '--query-path', dest='query_path',
                       action='store',
                       help='path to query json file')
    group.add_argument('-q', '--query', dest='query',
                       action='store',
                       help='string with json query')
    group.add_argument('-idsp', '--ids-path', dest='ids_path',
                       action='store',
                       help='a json contains list of ids')
    group.add_argument('-ids', '--ids', dest='ids', nargs='+',
                       action='store',
                       help='comma seperated list of ids')

    parser.add_argument('-dt', '--download-type', dest='download_type',
                        required=True, action='store',
                        help='type of download it can be '
                             'documents or live_videos or live_photos')

    parser.add_argument('-i', '--index', dest='index',
                        action='store',
                        help='The elastic search index')

    parser.add_argument('-rp', '--result-path',
                        dest='result_path',
                        action='store', default=os.getcwd(),
                        help='path to folder to download the files')

    parser.add_argument('-fn', '--folder-name',
                        dest='folder_name',
                        action='store', default='',
                        help='destination folder name if any')

    parser.add_argument('-dp', '--dotted-path', dest='dotted_path',
                        action='store', default=None,
                        help='nested path to the parent of the target key like live_photos_data.data '
                             'This can used in conjunction with --key, leave this arg '
                             'if key is at first level')

    parser.add_argument('-k', '--key', dest='key',
                        action='store', default=None,
                        help='your target key in dictionary or list document_id')

    parser.add_argument('--no-image',
                        dest='no_image',
                        action='store_true', default=False,
                        help='If active no image will be downloaded')

    parser.add_argument('-H', '--host', dest='host',
                        action='store',
                        default=HOST,
                        help='The elasticsearch host')

    parser.add_argument('-s', '--size', dest='size',
                        action='store',
                        type=int,
                        default=None,
                        help='The size of results to retrieve. '
                             'Defaults is all data queried')

    parser.add_argument('-rn', '--row-number', dest='row_number',
                        action='store', type=int,
                        help='row number')

    parser.add_argument('-nt', '--number-threads', dest='nthreads',
                        action='store',
                        default=20,
                        help='The number of parallel threads to '
                             'use when downloading. Defaults is 20')

    parser.add_argument('-r', '--region', dest='region',
                        action='store', default=DEFAULT_AWS_REGION,
                        help='The aws region to use. Defaults to {}'
                        .format(DEFAULT_AWS_REGION))

    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('--imago-dev',
                       dest='imago_dev',
                       action='store_true', default=False,
                       help='If active uses imago-dev url '
                            'to download resources')

    group1.add_argument('--media-provider',
                       dest='media_provider',
                       action='store_true', default=False,
                       help='If active uses media_provider url '
                            'to download resources')

    parser.add_argument('-p', '--profile', dest='aws_profile',
                        action='store',
                        default=None,
                        help='AWS profile, by default it reads '
                             'from ~/.aws/config ')

    return parser


def _create_results_directory(local_path, folder_name):

    if not folder_name:
        folder_name = datetime.now().strftime('%Y-%m-%dT%H-%m-%S')

    full_path = os.path.join(local_path, folder_name)

    return full_path


def _parse_arguments():
    """A function to parse the user's arguments and return an object which
    holds the user's parsed arguments.

    :return: The user's parsed arguments as object.
    """
    parser = _create_parser()
    args = parser.parse_args()
    return args


def create_output_dir(local_path, folder_name, download_type):
    """ create output directory

    :param local_path: load path
    :param folder_name: folder name
    :param download_type: download type
    :return: full local path
    """
    if not folder_name:
        folder_name = datetime.now().strftime('%Y-%m-%dT%H-%m-%S')

    full_path = join(local_path, folder_name)

    path = join(full_path, download_type)

    if not exists(path):
        try:
            os.makedirs(path)
        except:
            pass

    return full_path


def _load_query(query_path):
    """path to json query

    :param query_path:
    :return:
    """
    if not os.path.exists(query_path):
        raise ElasticSearchDownloader('Unable to find the file '
                                      'please check the path')
    try:
        with open(query_path, 'r') as query_file:
            query = json.load(query_file)
    except:
        raise ElasticSearchDownloader('Unable to load the file. '
                                      'check if json file is correct')

    return query


def download_from_es(query,
                     result_path,
                     index,
                     download_type,
                     size,
                     nthreads=20,
                     imago_dev=False,
                     media_provider=False,
                     host=HOST,
                     folder_name='',
                     no_image=False,
                     aws_profile=None,
                     dotted_path=None,
                     key=None):

    """ download from elasticsearch

    :param query: query in dictionary
    :param result_path: result path
    :param index: index name
    :param download_type: download type
    :param size: size
    :param imago_dev: use imago development
    :param host: host name
    :param folder_name: folder name
    :param no_image: no image downloaded
    :param nthreads: number of parallel threads
    :return: metadata result and query results
    """
    # Create es client
    es_client = create_es_client(host, aws_profile=aws_profile)

    # Form query/execute/retrieve results
    es_q = ESQuery(es_client, index, query, size=size)
    query_results, metadata_result = es_q.perform_query()

    # Create path
    full_path = create_output_dir(result_path, folder_name, download_type)

    # Download the links
    if no_image is False:
        # Build urls to download
        ids_urls = UrlBuilder(index=index, download_type=download_type, imago_dev=imago_dev,
                              media_provider=media_provider, dotted_path=dotted_path, key=key).\
            build_urls_with_query(query_results)

        id_info = download_files(ids_urls, download_type, full_path, nthreads)

        write_log_paths(id_info, full_path)

    # Write metadata
    write_meta_result_es(full_path, metadata_result, query_results)

    return metadata_result, query_results


def download_from_imago(ids, download_type, result_path,
                        folder_name='', nthreads=20, imago_dev=False,
                        media_provider=False, size=None, row_number=None):
    row_number = row_number - 1 if row_number else 0
    ids = ids[row_number:row_number + size] if size else ids[row_number:]

    # Create path
    full_path = create_output_dir(result_path, folder_name, download_type)

    urls_ids = UrlBuilder(download_type=download_type, imago_dev=imago_dev, media_provider=media_provider). \
        build_urls_no_query(ids)

    id_info = download_files(urls_ids, download_type, full_path, nthreads)

    write_log_paths(id_info, full_path)


def main():
    """main function"""
    imago_only = False
    arguments = _parse_arguments()

    if arguments.query_path:
        arguments.query = _load_query(arguments.query_path)

    elif arguments.query:
        arguments.query = json.loads(arguments.query)

    elif arguments.ids_path:
        if arguments.ids_path[-4:] == 'json':
            ids = _load_query(arguments.ids_path)['ids']
        else:
            ids = load_ids_file(arguments.ids_path)
        imago_only = True

    elif arguments.ids:
        ids = arguments.ids
        imago_only = True

    else:
        raise ElasticSearchDownloader(
            'Parameter missing: Please pass either query_path or  query')

    if imago_only:
        download_from_imago(ids=ids,
                            download_type=arguments.download_type,
                            result_path=arguments.result_path,
                            folder_name=arguments.folder_name,
                            nthreads=arguments.nthreads,
                            imago_dev=arguments.imago_dev,
                            media_provider=arguments.media_provider,
                            size=arguments.size,
                            row_number=arguments.row_number)
    else:
        if not arguments.index:
            raise ElasticSearchDownloader('index not provided!')

        download_from_es(query=arguments.query,
                         result_path=arguments.result_path,
                         index=arguments.index,
                         host=arguments.host,
                         nthreads=arguments.nthreads,
                         download_type=arguments.download_type,
                         size=int(arguments.size),
                         imago_dev=arguments.imago_dev,
                         media_provider=arguments.media_provider,
                         folder_name=arguments.folder_name,
                         no_image=arguments.no_image,
                         aws_profile=arguments.aws_profile,
                         dotted_path=arguments.dotted_path,
                         key=arguments.key)


if __name__ == '__main__':
    main()
