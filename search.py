from elastic_indexer import Indexer
import json
import re
def pp(obj):
	print(json.dumps(obj, indent=3))

class Search:
	def __init__(self, text, index="test", doc_type="test", hosts=None):
		self.indexer = Indexer(index=index, doc_type=doc_type, hosts=hosts)
		self.query = self._make_query(text)

	def _make_query(self, text):
		# ['filename', 'url', 'site_text', 'site_html', 'id', 'title', 'description', 'keywords', 'text']
		text2 = re.sub("\s+", " ", text)
		text2 = text2.strip().replace(" ", " OR " )
		
		return {
			"highlight": {
				"fields": {
					'title': {},
					'description': {},
					"site_text": {},
				}
			},
				"query": {
					"query_string": {
						"fields" : ["keywords^2", "site_text", "description^3", "title^4"],
						"query" : text2
					}
				}
				#"query": {
				#	"bool": {
				#		"should": [
				#			{
				#				"match_phrase": {
				#					"site_text": {
				#						"query": text
				#					}
				#				}
				#			},
				#			{
				#				"match_phrase": {
				#					"title": {
				#						"query": text,
				#						"boost": 4
				#					}
				#				}
				#			},
				#			{
				#				"match_phrase": {
				#					"description": {
				#						"query": text,
				#						"boost": 3
				#					}
				#				}
				#			},
				#			{
				#				"match_phrase": {
				#					"keywords": {
				#						"query": text,
				#						"boost": 2
				#					}
				#				}
				#			}
				#		]
				#	}
				#}
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
		return self.indexer.search(self.query, source=['title', 'url'])

if __name__ == "__main__":
	s = Search('basketball')
	pp(s.search())

	s = Search('national basketball association')

	pp(s.search())