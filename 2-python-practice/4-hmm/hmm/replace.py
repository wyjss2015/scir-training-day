import sys
import re

def reader(corpus_file):
	line = corpus_file.readline()
	while line:
		field = line.strip().split()
		if field:
			yield (field[0],field[1])
		else:
			yield (None,None)
		line = corpus_file.readline()

class replacer(object):
	def __init__(self):
		self.counts = {}

	def replace_count(self,corpus_file):
		word_label = reader(corpus_file)
		for word,label in word_label:
			if word:
				if word not in self.counts:
					self.counts[word] = 1
				else:
					self.counts[word] += 1
		for key in self.counts.keys():
			if self.counts[key] >= 5:
				del self.counts[key]
	
	def replace_rare(self, corpus_file, output_file):
		word_label = reader(corpus_file)
		for word,label in word_label:
			if word:
				if word in self.counts:
					output_file.write('_RARE_ '+label+'\n')
				else:
					output_file.write(word+' '+label+'\n')
			else:
				output_file.write('\n')
	

if __name__ == '__main__':
	input_file1 = open(sys.argv[1],'r')
	input_file2 = open(sys.argv[1],'r')
	output_file = open(sys.argv[2],'w')

	rep = replacer()
	rep.replace_count(input_file1)
	rep.replace_rare(input_file2, output_file)
