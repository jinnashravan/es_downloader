"""query builder"""
import copy

from elasticsearch import helpers

from es_downloader.exception import NoResultsException


class ESQuery(object):
    """ES query builder/executor"""
    def __init__(self, es_client, index, query, size=0):
        self.es_client = es_client
        self.index = index
        self.size = int(size)
        self.query = query

    def perform_query(self):
        """run the query and prepare/return the results"""
        results = self._query_es()
        metadata_result = self._get_metadata_result(results[0], self.size)
        query_result = self._get_query_results(results)

        return query_result, metadata_result

    def _query_es(self):
        """query the elastic saerch"""
        print('Querying Elastic Search. Please wait...')
        results = helpers.scan(
            self.es_client,
            self.query,
            index=self.index)

        new_res = list()
        for no, res in enumerate(results, 1):
            new_res.append(res)

            if no == self.size:
                break

        self.size = len(new_res)

        if not new_res:
            raise NoResultsException(
                'Your query did not return any results. '
                'Check the names of fields and the operators')

        return new_res

    @staticmethod
    def _get_metadata_result(result, size):
        """get the metadata result """
        new_res = copy.deepcopy(result)
        _ = [new_res.pop(i) for i in ['_source', '_id', 'sort']
             if i in new_res]

        new_res['size'] = size
        return new_res

    @staticmethod
    def _get_query_results(results):
        """return result of query """
        return [result['_source'] for result in results]
