from elastic_indexer import Indexer
import json

def pp(obj):
	print(json.dumps(obj, indent=3))

class Search:
	def __init__(self, text, index="test", doc_type="test", hosts=None):
		self.indexer = Indexer(index=index, doc_type=doc_type, hosts=hosts)
		self.query = self._make_query(text)

	def _make_query(self, text):
		return {
			"highlight": {
				"fields": {
					"site_text": {}
				}
			},
			"query": {
				"match_phrase": {
					"site_text": text
				}
			}
		}

	def _match_all(self):
		return {
			'_source': 'text',
			'query': {
				'match_all': {
				}
			}
		}

	def search(self):
		return self.indexer.search(self.query)

if __name__ == "__main__":
	s = Search('basketball')
	pp(s.search())

	s = Search('national basketball association')

	pp(s.search())

