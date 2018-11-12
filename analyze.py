import re
import os
import itertools
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit

class Analyze:
	def __init__(self):
		self.repo = 'processed'
		self.counter = Counter([])
		self.process_text()

	def process_text(self):
		for filename in os.listdir(self.repo):
			with open(os.path.join(self.repo, filename), 'r') as f:
				text = f.read().lower()
				word_list = re.findall(r'\w+', text)
				self.counter += Counter(word_list)

		# orders by highest frequency
		self.counter = self.counter.most_common(len(self.counter))

		self.ranks = range(1, len(self.counter) + 1)
		self.frequencies = []
		self.most_frequent_words = []
		for i, (word, frequency) in enumerate(self.counter):
			if i < 100:
				self.most_frequent_words.append(word)
			self.frequencies.append(frequency)
		self.total_words = sum(self.frequencies)
		self.probabilities = [(self.frequencies[i]/self.total_words)*self.ranks[i] for i in range(100)]


	def plot_graph(self, title):
		x = np.log(np.array(self.ranks))
		y = np.log(np.array(self.frequencies))

        # intercept (b) and slope (m) for best fit line of scatter plot
		b, m = polyfit(x, y, 1)

		plt.plot(x,y,'.')
		plt.plot(x,b+m*x,'-')
		plt.title(title)
		plt.xlabel('log(rank)')
		plt.ylabel('log(frequency)')
		plt.show()

	def plot_most_frequent(self):
		data = np.array([self.most_frequent_words, self.ranks[:100], self.frequencies[:100], self.probabilities]).transpose()

		fig, axes = plt.subplots(1,1)
		collabel = ('Words', 'Rank', 'Frequency', 'rPr')
		axes.axis('tight')
		axes.axis('off')
		table = axes.table(cellText=data,colLabels=collabel,loc='center')
		table.set_fontsize(28)
		table.scale(2, 2)
		fig.show()
