"""url builder"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from es_downloader.config import IMAGO_DOC_URL, \
    IMAGO_LIVE_VIDEO_URL, \
    DOWNLOAD_TYPE_DOC, DOWNLOAD_TYPE_LIVE_IMG, \
    DOWNLOAD_TYPE_LIVE_VID, IMAGO_LIVE_PHOTOS_URL, \
    IMAGO_DOC_URL_METADATA, IMAGO_LIVE_PHOTOS_URL_METADATA, \
    IMAGO_LIVE_VIDEO_URL_METADATA, MEDIA_PROVIDER_DOC_URL, \
    MEDIA_PROVIDER_LIVE_PHOTOS_URL, MEDIA_PROVIDER_LIVE_VIDEO_URL
from es_downloader.exception import ElasticSearchDownloader
from es_downloader.utils import find_item_dict


class UrlBuilder(object):
    """UrlBuilder class"""
    def __init__(self, download_type, index=None, imago_dev=False,
                 media_provider = False, dotted_path=None,
                 key=None, metadata_url=False):
        self.index = index
        self.download_type = download_type
        self.imago_dev = imago_dev
        self.media_provider = media_provider
        self.dotted_path = dotted_path
        self.key = key
        self.metadata_url = metadata_url  # If True, downloads Image metadata

    def build_urls_no_query(self, ids):
        """build urls

        :return: urls
        """
        url_template = self._get_url_template()

        ids_urls = dict()
        for _id in ids:
            url = url_template.format(id=_id)
            ids_urls[_id] = url

        return ids_urls

    def build_urls_with_query(self, query_results):
        """build urls

        :param query_results: query results
        :return: urls
        """
        url_template = self._get_url_template()
        ids = self._get_ids(query_results)

        ids_urls = dict()
        for _id in ids:
            url = url_template.format(id=_id)
            ids_urls[_id] = url

        return ids_urls

    def _get_url_template(self):
        """get url template

        :return: imago url template
        """
        if self.media_provider:
            if self.download_type == DOWNLOAD_TYPE_DOC:
                source_url = MEDIA_PROVIDER_DOC_URL
            elif self.download_type == DOWNLOAD_TYPE_LIVE_IMG:
                source_url = MEDIA_PROVIDER_LIVE_PHOTOS_URL
            elif self.download_type == DOWNLOAD_TYPE_LIVE_VID:
                source_url = MEDIA_PROVIDER_LIVE_VIDEO_URL
        else:
            if self.download_type == DOWNLOAD_TYPE_DOC:
                if self.metadata_url:
                    imago_url = IMAGO_DOC_URL_METADATA
                else:
                    imago_url = IMAGO_DOC_URL
            elif self.download_type == DOWNLOAD_TYPE_LIVE_IMG:
                if self.metadata_url:
                    imago_url = IMAGO_LIVE_PHOTOS_URL_METADATA
                else:
                    imago_url = IMAGO_LIVE_PHOTOS_URL
            elif self.download_type == DOWNLOAD_TYPE_LIVE_VID:
                if self.metadata_url:
                    imago_url = IMAGO_LIVE_VIDEO_URL_METADATA
                else:
                    imago_url = IMAGO_LIVE_VIDEO_URL
            else:
                raise ElasticSearchDownloader('Unsupported download type')

            if self.imago_dev:
                source_url = imago_url.format(imago='imago-dev')
            else:
                source_url = imago_url.format(imago='imago')

        return source_url

    def _get_ids(self, query_results):
        """get a list of documents/photos/videos

        :param query_results: results of query
        :return: list of ids
        """
        doc_ids = list()
        # IMPORT: For backward compatibility we keep this if
        # should be deprecated in future
        if self.key is None:
            if self.download_type == DOWNLOAD_TYPE_DOC:
                if self.index.startswith('platform'):
                    self.dotted_path = 'documents_data'
                    self.key = 'document_id'

                else:
                    self.dotted_path = None
                    self.key = 'document_id'

            elif self.download_type == DOWNLOAD_TYPE_LIVE_IMG and \
                    self.index.startswith('platform'):
                self.dotted_path = 'live_photos_data'
                self.key = 'live_photo_id'

            elif self.download_type == DOWNLOAD_TYPE_LIVE_VID and \
                    self.index.startswith('platform'):
                self.dotted_path = 'live_videos_data'
                self.key = 'live_video_id'

        if self.key is None:
            raise ElasticSearchDownloader('Please provide dotted path and key!')

        for result in query_results:
            res_dict, self.key = find_item_dict(result, self.dotted_path, self.key)

            if isinstance(res_dict, list):
                [doc_ids.append(item.get(self.key)) for item in res_dict if self.key in item]
            else:
                if res_dict.get(self.key):
                    doc_ids.append(int(float(res_dict.get(self.key))))

        return doc_ids
