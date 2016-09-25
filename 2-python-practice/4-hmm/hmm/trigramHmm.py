from __future__ import division
import sys

def reader(corpus_file):
	line = corpus_file.readline()
	while line:
		field = line.strip().split()
		if field:
			yield field
		line = corpus_file.readline()

def sentence_reader(input_file):
	line = input_file.readline()
	sentence = []
	while line:
		word = line.strip()
		if word:
			sentence.append(word)
		else:
			yield sentence
			sentence = []
		line = input_file.readline()

class hmm(object):
	def __init__(self):
		self.emissions = {}
		self.transitions = {}
		self.unigram = {}
		self.bigram = {}
		self.tags = []
		self.all_status = ['O','I-GENE']

	def train(self, counts_file):
		freq_counts = reader(counts_file)
		for freq in freq_counts:
			if freq:
				if freq[1] == 'WORDTAG':
					tmp = {}
					tmp[freq[2]] = int(freq[0])
					if freq[-1] in self.emissions:
						self.emissions[freq[-1]].update(tmp)
					else:
						self.emissions[freq[-1]] = tmp
				elif freq[1] == '1-GRAM':
					self.unigram[freq[-1]] = int(freq[0])
				elif freq[1] == '2-GRAM':
					tmp = {}
					tmp[freq[-1]] = int(freq[0])
					if freq[2] in self.bigram:
						self.bigram[freq[2]].update(tmp)
					else:
						self.bigram[freq[2]] = tmp
				else:
					tmp = {}
					tmp[freq[-1]] = int(freq[0])
					if freq[2] in self.transitions:
						if freq[3] in self.transitions[freq[2]]:
							self.transitions[freq[2]][freq[3]].update(tmp)
						else:
							self.transitions[freq[2]][freq[3]] = tmp
					else:
						tmp2 = {}
						tmp2[freq[3]] = tmp
						self.transitions[freq[2]] = tmp2
		for i in self.emissions:
			for j in self.emissions[i]:
				self.emissions[i][j] /= self.unigram[j]
		for word in self.emissions:
			if 'O' not in self.emissions[word]:
				self.emissions[word]['O'] = 0.0
			elif 'I-GENE' not in self.emissions[word]:
				self.emissions[word]['I-GENE'] = 0.0
		for i in self.transitions:
			for j in self.transitions[i]:
				for k in self.transitions[i][j]:
					self.transitions[i][j][k] /= self.bigram[i][j]

	def make_tags(self,pi,bp,n):
		if n == 1:
			maxVal = -1.0
			tmpTag = ''
			for step,i,j in pi.keys():
				tmp = pi[(step,i,j)]*self.transitions['*'][j]['STOP']
				if tmp > maxVal:
					maxVal = tmp
					tmpTag = j
			self.tags.append([tmpTag])
		else:
			maxVal = -1.0
			for i in self.all_status:
				for j in self.all_status:
					tmp = pi[(n-1,i,j)]*self.transitions[i][j]['STOP']
					if tmp>maxVal:
						maxVal = tmp
						p = i
						q = j
			tmpTags = [p,q]
			l = [q,p]
			k = n-1
			while k>1:
				r = bp[(k,p,q)]
				l.append(r)
				q = p
				p = r
				k -= 1
			l.reverse()
			self.tags.append(l)

	def viterbi(self, sentence):
		n = len(sentence)
		rare_words = []
		pi = {}
		bp = {}
		for word in sentence:
			if word not in self.emissions:
				rare_words.append('_RARE_')
			else:
				rare_words.append(word)
		step = 0
		while step<n:
			if step == 0:
				pi[(step,'*','O')] = self.transitions['*']['*']['O']*self.emissions[rare_words[step]]['O']
				pi[(step,'*','I-GENE')] = self.transitions['*']['*']['I-GENE']*self.emissions[rare_words[step]]['I-GENE']

			elif step == 1:
				for i in self.all_status:
					for j in self.all_status:
						pi[(step,i,j)] = pi[(step-1,'*',i)]*self.transitions['*'][i][j]*self.emissions[rare_words[step]][j]
			else:
				for i in self.all_status:
					for j in self.all_status:
						pi[(step,i,j)] = -1.0
						for k in self.all_status:
							tmp = pi[(step-1,k,i)]*self.transitions[k][i][j]*self.emissions[rare_words[step]][j]
							if tmp>pi[(step,i,j)]:
								pi[(step,i,j)] = tmp
								bp[(step,i,j)] = k
			step += 1
		self.make_tags(pi,bp,n)
			
		
	def tag(self,input_file):
		sentences = sentence_reader(input_file)
		for sentence in sentences:
			self.viterbi(sentence)

if __name__ == '__main__':
	input_file = open(sys.argv[1],'r')
	input_file1 = open(sys.argv[1],'r')
	counts_file = open(sys.argv[2],'r')
	output_file = open(sys.argv[3],'w')

	tagger = hmm()
	tagger.train(counts_file)
	tagger.tag(input_file)
	
	sentences = sentence_reader(input_file1)
	for sentence,tags in zip(sentences, tagger.tags):
		for word, tag in zip(sentence, tags):
			output_file.write(word+' '+tag+'\n')
		output_file.write('\n')
		
