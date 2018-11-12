from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.client import IndicesClient


class Indexer:
    def __init__(self, index, doc_type, hosts=None):
        if hosts is None:
            hosts = ['localhost']

        self.es = Elasticsearch(hosts=hosts, verify_certs=False, timeout=60)
        self.ic = IndicesClient(self.es)
        self.index = index
        self.doc_type = doc_type

    def list_indices(self):
        '''
        Lists the indices present on the elastic cluster
        '''
        indices = self.es.indices.get_alias()
        return indices.keys()

    def search(self, body, size=1000, source=False, from_=0):
        '''
        Searches on the given index - see Query language for body parameter
        '''
        return self.es.search(index=self.index, doc_type=self.doc_type, body=body, size=size, _source=source, from_=from_)

    def create_empty_index(self):
        """
        Creates an empty ES index if it doesn't exist already
        """
        self.es.indices.create(index=self.index, ignore=400)

    def create_index(self, body):
        '''
        Creates an index with optional mapping and settings through body param
        '''
        self.es.indices.create(index=self.index, ignore=400, body=body)

    def delete_index(self):
        '''
        Deletes the given index
        '''
        self.es.indices.delete(index=self.index, ignore=[400, 404])

    def put_mapping(self, body):
        '''
        Puts a mapping on the given index. Only can be done once per indec
        '''
        return self.es.indices.put_mapping(body=body, index=self.index, doc_type=self.doc_type)

    def get_mapping(self):
        '''
        Gets the mapping for the given index
        '''
        return self.ic.get_mapping(index=self.index, doc_type=self.doc_type)

    def put_settings(self, settings):
        return self.ic.put_settings(body=settings, index=self.index)

    def get_settings(self):
        return self.ic.get_settings(index=self.index)

    def index_data(self, data):
        '''
        Index one document to the given index
        Document must include an 'id' key
        '''
        result = self.es.index(index=self.index, doc_type=self.doc_type, id=data['id'], body=data)
        return result

    def bulk_index_data(self, data, bulk_items_per_request=6):
        '''
        Index mulitple documents to the given index
        Each document must include an 'id' key
        '''
        b_count = 0

        bulk_items_cntr = 0
        actions = list()

        for i, datum in enumerate(data):
            bulk_items_cntr += 1
            actions.append(
                {
                    '_op_type': "index",
                    "_index": self.index,
                    "_type": self.doc_type,
                    "_id": datum["id"],
                    "_source": datum
                }
            )
            if bulk_items_cntr > bulk_items_per_request:
                print ("Bulking")
                helpers.bulk(self.es, actions, stats_only=True)
                bulk_items_cntr = 0
                actions = []

        if len(actions) != 0:
            print ("Final Bulking")
            helpers.bulk(self.es, actions, stats_only=True)


if __name__ == "__main__":
    import lorem
    indexer = Indexer(index='test', doc_type='test')
    indexer.create_empty_index()
    indexer.index_data({'id': 1, 'name': 'John Doe'})
    result = indexer.search({'query': {
        'match': {'name': 'John'}
        }}, source='name')
    print(indexer.get_mapping())
    print(indexer.get_settings())

    data = [{'id': i, 'name': v} for i,v in enumerate(lorem.paragraph().split(' '))]

    indexer.bulk_index_data(data)

    result = indexer.search({'query': {'match_all': {}}})
    print(result['hits']['total'])


