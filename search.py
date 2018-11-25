from elastic_indexer import Indexer
import json

def pp(obj):
	print(json.dumps(obj, indent=3))

class Search:
	def __init__(self, text, negative, index="test", doc_type="test", hosts=None):
		self.indexer = Indexer(index=index, doc_type=doc_type, hosts=hosts)
		self.query = self._make_query(text, negative)

	def _make_query(self, text, negative):
		# ['filename', 'url', 'site_text', 'site_html', 'id', 'title', 'description', 'keywords', 'text']
		return {
			"highlight": {
				"fields": {
					"site_text": {}
				}
			},

				"query": {
					"bool": {
						"must_not": [
							{
								"match_phrase": {
									"site_text": {
										"query": negative
									}
								}
							},
							{
								"match_phrase": {
									"title": {
										"query": negative,
										"boost": 4
									}
								}
							},
							{
								"match_phrase": {
									"description": {
										"query": negative,
										"boost": 3
									}

								}
							},
							{
								"match_phrase": {
									"keywords": {
										"query": negative,
										"boost": 2
									}

								}
							}
						],
						"should": [
							{
								"match_phrase": {
									"site_text": {
										"query": text
									}
								}
							},
							{
								"match_phrase": {
									"title": {
										"query": text,
										"boost": 4
									}
								}
							},
							{
								"match_phrase": {
									"description": {
										"query": text,
										"boost": 3
									}

								}
							},
							{
								"match_phrase": {
									"keywords": {
										"query": text,
										"boost": 2
									}

								}
							}
						]
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

