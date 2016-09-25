from __future__ import division
import sys

def reader(corpus_file):
	line = corpus_file.readline()
	while line:
		field = line.strip().split()
		yield field
		line = corpus_file.readline()

class ep(object):
	def __init__(self):
		self.label_count = {}
		self.word_count = {}

	def count(self,corpus_file):
		freq_counts = reader(corpus_file)
		for freq in freq_counts:
			if freq:
				if freq[1] == 'WORDTAG':
					tmp = {}
					tmp[freq[2]] = int(freq[0])
					if freq[-1] in self.word_count:
						self.word_count[freq[-1]].update(tmp)
					else:
						self.word_count[freq[-1]] = tmp
				elif freq[1] == '1-GRAM':
					self.label_count[freq[-1]] = int(freq[0])
		for key in self.word_count:
			for key1 in self.word_count[key]:
				self.word_count[key][key1] = self.word_count[key][key1]/self.label_count[key1]

if __name__ == '__main__':
	ep_file = open(sys.argv[2],'r')
	input_file = open(sys.argv[1],'r')
	output_file = open(sys.argv[3],'w')

	emission = ep()
	emission.count(ep_file)
	
	for line in input_file:
		word = line.strip()
		tmpWord = word
		if word:
			if word not in emission.word_count:
				word = '_RARE_'
			label_sort = sorted(emission.word_count[word].iteritems(),key=lambda x:x[1],reverse=True)
			output_file.write(tmpWord+' '+label_sort[0][0]+'\n')
		else:
			output_file.write('\n')
