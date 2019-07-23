"""config file"""
import os


def get_media_provider_url():
    if os.environ.get('MEDIA_PROVIDER_SERVICE_HOST'):
        url = 'http://{}:{}/silo'.format(
            os.environ.get('MEDIA_PROVIDER_SERVICE_HOST'), os.environ.get('MEDIA_PROVIDER_SERVICE_PORT'))
    else:
        url = 'https://media-provider.eu-west-1.citrix.onfido.xyz/silo'

    return url


DEFAULT_RESULTS_SIZE = 100
DEFAULT_AWS_REGION = 'eu-west-1'
QUERY_RESULTS_FILE = 'query_results.json'
METADATA_RESULTS_FILE = 'metadata_results.json'
LOCATION_PATH_FILE = 'file_paths_{}.json'
DOC_TYPES = ['documents']
HOST = 'search-tf-data-pipeline-dqqa4672d4jyeyvcny6txizlea.eu-west-1.es.amazonaws.com'   # pylint: disable=line-too-long
INDEX_NAME = 'document-labels-production'

MEDIA_PROVIDER_DOC_URL = "{}/documents/{{id}}/download".format(get_media_provider_url())  # pylint: disable=line-too-long
MEDIA_PROVIDER_LIVE_PHOTOS_URL = "{}/live_photos/{{id}}/download".format(get_media_provider_url())   # pylint: disable=line-too-long
MEDIA_PROVIDER_LIVE_VIDEO_URL = "{}/live_videos/{{id}}/download".format(get_media_provider_url())   # pylint: disable=line-too-long

IMAGO_DOC_URL = "https://{imago}.onfido.com/api/documents/{{id}}/download"  # pylint: disable=line-too-long
IMAGO_LIVE_PHOTOS_URL = "https://{imago}.onfido.com/api/live_photos/{{id}}/download"  # pylint: disable=line-too-long
IMAGO_LIVE_VIDEO_URL = "https://{imago}.onfido.com/api/live_videos/{{id}}/download"  # pylint: disable=line-too-long

IMAGO_DOC_URL_METADATA = "https://{imago}.onfido.com/api/documents/{{id}}"  # pylint: disable=line-too-long
IMAGO_LIVE_PHOTOS_URL_METADATA = "https://{imago}.onfido.com/api/live_photos/{{id}}"  # pylint: disable=line-too-long
IMAGO_LIVE_VIDEO_URL_METADATA = "https://{imago}.onfido.com/api/live_videos/{{id}}"  # pylint: disable=line-too-long

DOWNLOAD_TYPE_DOC = 'documents'
DOWNLOAD_TYPE_LIVE_IMG = 'live_photos'
DOWNLOAD_TYPE_LIVE_VID = 'live_videos'
