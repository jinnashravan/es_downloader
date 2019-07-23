"""file downloader"""
import re

import concurrent.futures as ft
from os.path import exists
import requests
from tqdm import tqdm


def _download_one(url, folder_path, download_type):
    r = requests.get(url, stream=True)
    file_path = None
    if r.status_code == 200:
        d = r.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)[0].replace('"', '').replace("'", '')  # pylint: disable=line-too-long

        file_path = '{0}/{1}/{2}'.format(folder_path, download_type, fname)
        if not exists(file_path):
            with open(file_path, 'wb') as fd:
                fd.write(r.content)

    return file_path


def download_files(ids_urls, download_type, full_path, nthreads=20):
    """download resources for a list of urls

    :param urls: list of urls
    :param download_type: download type can br 'documents or live_photo etc'
    :param full_path: full local path
    :param nthreads: number of threads
    """
    tuples = []
    print('Downloading resources into: {}'.format(full_path))
    for id, url in ids_urls.items():
        tp = (url, full_path, download_type, id)
        tuples.append(tp)

    with ft.ThreadPoolExecutor(max_workers=nthreads) as executor:
        # Start the load operations and mark each future with its URL
        future_paths = {
            executor.submit(_download_one, url, fp, dt): (id, url, dt)
            for url, fp, dt, id in tuples
            }

        id_info = dict()
        for future in tqdm(ft.as_completed(future_paths.keys())):
            path = future.result()
            id, url, dt = future_paths[future]
            if path:
                id_info[id] = dict()
                id_info[id]['url'] = url
                id_info[id]['path'] = path
                id_info[id]['dtype'] = dt

    print('Total number of {} downloaded : {}'.format(
        download_type, len(id_info)))

    return id_info
