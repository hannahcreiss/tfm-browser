from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class DisplayInfo:
	def __init__(self, todo):
		self.url = todo.description

	def get_soup(self):
		req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
		data = urlopen(req).read()
		# parse as html structured document
		bs = BeautifulSoup(data,'html.parser')# kill javascript content
		for s in bs.findAll('script'):
			s.replaceWith('')	
		self.soup = bs    

	def get_title(self):
		title = self.soup.find("h1", class_="entry-title")
		self.title = title.text

	def get_comments(self):
		commentDivs = self.soup("div", class_="comment-content")
		self.comments = []
		for div in commentDivs:
			score = int(div.find_previous_sibling("span").text)
			content = div.p.text
			newComment = Comment(score,content)
			self.comments.append(newComment)	
		self.comments.sort(key = lambda c: c.score, reverse=True)
		for comment in self.comments:
			print("score: ")
			print(comment.score)
			print("content: ")
			print(comment.content)


class Comment:
	def __init__(self, score, content):
		self.score = score
		self.content = content

