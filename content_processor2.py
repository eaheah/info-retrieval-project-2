from newspaper import Article

class ContentProcessor:
	def __init__(self, html):
		self.article = Article(url='')
		self.article.set_html(html)
		self.article.parse()

if __name__ == '__main__':
	with open('repository/1.html', 'rb') as f:
		html = f.read()
	cp = ContentProcessor(html)
	print(cp.article.title)