from newspaper import Article, fulltext
import html2text
import urllib
import os


class ContentProcessor:
	def __init__(self, html):
		self.article = Article(url='')
		self.article.set_html(html)

	def extract_fields(self):
		self.article.parse()
		self.article.nlp()

		return {
			"title": self.article.title,
			"description": self.article.meta_description,
			"keywords": self.article.meta_keywords + self.article.keywords,
			"text": self.article.text
		}

if __name__ == '__main__':
	with open('repository/1.html', 'rb') as f:
		html = f.read()
	cp = ContentProcessor(html)
	print(cp.extract_fields())

