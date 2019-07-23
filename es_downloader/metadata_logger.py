import json
from os.path import join
import uuid

import os

from es_downloader.config import QUERY_RESULTS_FILE, METADATA_RESULTS_FILE, LOCATION_PATH_FILE
from es_downloader.utils import write_file


def write_meta_result_es(full_path, metadata_result, query_results):
    """write query result in file

    :param full_path:
    :param metadata_result:
    :param query_results:
    """
    # write results
    path = join(full_path, QUERY_RESULTS_FILE)
    write_file(path, query_results)

    # write meta
    path = join(full_path, METADATA_RESULTS_FILE)
    write_file(path, metadata_result)

    print('You can find the result here: {}'.format(full_path))


def get_size(file_path):
    """get size of file"""
    st = os.stat(file_path)
    return st.st_size


def write_log_paths(id_info, full_path):
    """write file info to a json file """
    for id, info in id_info.items():
        info['size'] = get_size(info['path'])

    rnd = str(uuid.uuid4())[:8]
    log_path = join(full_path, LOCATION_PATH_FILE.format(rnd))
    with open(log_path, 'w+') as outfile:
        json.dump(id_info, outfile, indent=4)

