===============================
Elastic Search Downloader
===============================

Command line tool for download data from Elastic search.

Installing
==========

.. code-block:: shell

	$ pip install --extra-index-url http://pypi.onfido.co.uk:8080/simple es-downloader --trusted-host pypi.onfido.co.uk


Options
=======
.. code-block:: shell

  optional arguments:
  -h, --help            show this help message and exit

  **(Mandatory)**
  -qp QUERY_PATH, --query-path QUERY_PATH
                        the path to query json file
  **OR**
  -q QUERY, --query QUERY
                        string with json query


  -dt DOWNLOAD_TYPE, --download-type DOWNLOAD_TYPE
                        type of download it can be documents or live_videos or live_photos

  -i INDEX, --index INDEX The elastic search index name you want to query

  **(Optional)**
  -rp RESULT_PATH, --result-path RESULT_PATH
                        local path to the folder to download the files

  -fn FOLDER_NAME, --folder-name FOLDER_NAME
                        destination folder name if any otherwise todays date will be assigned as folder name

  --imago-dev           If active uses imago-dev URL to download resources

  --no-image            If active no image will be downloaded

  -H HOST, --host HOST  The elastic search host default is the current es cluster in prod
  
  -nt NTHREADS, --number-threads NTHREADS  The number of parallel threads to use when downloading. Default is `20`

  -s SIZE, --size SIZE  The size of results to be retrieved. Default size is all the queried data

  -r REGION, --region REGION The AWS region to use. Default is `eu-west-1`

   -p AWS_PROFILE, --profile AWS_PROFILE
                        AWS profile, by default it reads from ~/.aws/config

Important
=========
From v0.1.1 you can bypass ES and directly download images if you know the ids. for that refer to below section `No Elastic Search`

How to use it in cmd
====================
NOTE: Query path and download types arguments are required.

-  Download **documents** (images - label data) into a given directory - folder will be created using the current time

 .. code-block:: shell

        es-downloader -qp path/to/query.json -rp /result/path/dir -dt documents -i documentlabels --size 5

-  Download **live photo** into a given directory with given folder name.

 .. code-block:: shell

        es-downloader -qp path/to/query.json -rp /result/path/dir -fn folder_name -dt live_photos --size 5 -i platformreports --profile Development

-  Download **live videos** into a given directory

 .. code-block:: shell

  es-downloader -q path/to/query.json -rp /result/path/dir -dt live_videos --size 5 -i platformreports --imago-dev

- Perform a normal search query and get the results as a json locally.

 .. code-block:: shell

 es-downloader -q '{"query": ..... }' -rp . -dt documents -i some-index --size 5  --no-image

How to use it in python code
============================

1) You need to import the function.

2) Pass the above parameters. Following is the signature of the function

 .. code-block:: shell

   query = json.loads(query_file)
   download_from_es(query=...,
                     result_path=...,
                     index=...,
                     download_type=...,
                     size=...,
                     imago_dev=...,
                     folder_name=...,
                     aws_profile=...)

Here is an example of how it is used:

 .. code-block:: shell

  from es_downloader.main import download_from_es
  import json

  queryObj = json.loads(query_file)
  download_from_es(query=queryObj, result_path='/tmp', index='platformreports', download_type='live_photos', size=5)


Result structure
================

The will be a folder(-fn parameters or todays date), created under result_path.

 .. code-block:: shell

 ~ ls -l /tmp/2017-12-04T13-12-36/

 drwxrwxr-x 2 hamed hamed 4096 Dec  4 13:33 live_photos

 -rw-rw-r-- 1 hamed hamed   77 Dec  4 13:33 metadata_results.json

 -rw-rw-r-- 1 hamed hamed 6179 Dec  4 13:33 query_results.json


It includes the followings:

- metadata_results.json contains some metadata regarding the query results, such as index name, doc type, etc. (Mostly for internal use of the following script)

- **query_results.json** contains the actual data from elasticsearch based on the query provided

- **documents:** contains documents images (**if -dt or --download-type documents option passed**)

- **live_photos:** contains live photos (**if -dt or --download-type live_videos option passed**)

- **live_videos:** contains live videos (**if -dt or --download-type live_photos option passed**)

Query json example
==================

documents
---------

 .. code-block:: shell

  {"query": {"bool": {"must": [{"match": {"doc_properties.doc_type": {"query": "National Identity Card", "type": "phrase"}}}, {"match": {"project_id": {"query": "24", "type": "phrase"}}}, {"match": {"doc_properties.doc_country": {"query": "fra", "type": "phrase"}}}, {"nested": {"path": "fields", "query": {"bool": {"must": [{"match": {"fields.label": "first_name"}}]}}}}, {"nested": {"path": "fields", "query": {"bool": {"must": [{"match": {"fields.label": "last_name"}}]}}}}]}}}


live photos
-----------

 .. code-block:: shell

  {"query":{"bool":{"should":[{"nested":{"path":"live_photos_data","query":{"exists":{"field":"live_photos_data.live_photo_id"}}}}]}}}

live videos
-----------

 .. code-block:: shell

  {"query":{"bool":{"should":[{"nested":{"path":"live_videos_data","query":{"exists":{"field":"live_videos_data.live_video_id"}}}}]}}}

The resource id has different path/name
---------------------------------------
To be able to download images/videos with different name other than document_id, you can alternatively pass the path to the id in your data and the key which is the name of your resource identifier.
example:

```
        {
            "task_id": 309362,
            "timestamp": "2018-11-13T16:04:35",
            "created_at": "2018-11-02T15:50:52.060Z",
            "updated_at": "2018-11-13T15:55:30.248Z",
            "questions": [
              {
                "response_type": "odp",
                "free_text": "",
                "response": "originalDoc"
              }
            ],
            "test_field":
                "images": [
                  {
                    "identifier": "1111111111",
                    "component_type": "documents"
                  }
                ],
            "project_id": 195,
            "data_src_id": "QBL_production"
          }
```

In this example the resource id is called `identifier` and it is under `test_field.images` field you can pass the following arguments to the query:

    .. code-block:: shell

        es-downloader -qp ... -dp test_field.images -k identifier


No Elastic Search
=================
If you know the ids of the images/videos you can download them straight away.

You can do that in two ways:

Pass as argument
----------------

.. code-block:: shell

    es-downloader -ids 000 123 1234 -dt documents

Pass the file
-------------
you can pass a file contains a list of ids. Two types of files are accepted:

1)JSON file: contains a dictionary like

    .. code-block:: shell

        {
          "ids": [000, 123, 1234, 12345]
        }

2)A text file contains each id in one line:

    .. code-block:: shell

        000
        123
        1234
        12345

Example:

    .. code-block:: shell

        es-downloader -idsp test_ids -dt documents


Other options
-------------
- Pass a row number: you can download a subset of items in you file by passing row number and size
    Example:

    .. code-block:: shell

        es-downloader -idsp test_ids.json -dt documents -rn 2 --size 3


Get the project
===============

	1. Clone the git repository

	.. code-block:: shell

		$ git clone https://bitbucket.org/onfido/es_downloader

	2. Install a virtualenv

	.. code-block:: shell

		$ sudo apt-get install python-virtualenv

	3. Create a new virtualenv

	.. code-block:: shell

		$ virtualenv es_downloader_ve

	4. Install project's requirements

	.. code-block:: shell

		$ es_downloader_ve/bin/pip install -r requirements.txt



Reporting Issues
================
If you have suggestions, bugs or other issues specific to this library, open
an issue, or just be awesome and make a pull request out of it.

Maintainer
==========
**Document Extraction Team**

For other projects: check here https://wiki.onfido.co.uk/display/ENG/What+we+maintain
