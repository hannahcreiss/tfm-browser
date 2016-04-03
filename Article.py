class Article:
	def __init__(self, soup):
		self.soup = soup

	def add_author(self):
		a = self.soup.find('a', rel = 'author')
		self.author = a.text	

	def add_title(self):
		title = self.soup.find("h1", class_="entry-title")
		self.title = title.text
