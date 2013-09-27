def ngram(n, words):
    for i in xrange(len(words)-n+1):
        yield words[i:i+n]

def getWords(filename):
	words = []
	with open(filename) as f:
		for line in f.readlines():
			words += line.split()
	return words

def frequencyTop(top_n, words):
	from collections import Counter
	return Counter(map(tuple, words)).most_common(top_n)

if __name__ == "__main__":

	print frequencyTop(5, ngram(1, getWords("big-seg.txt")))
	print frequencyTop(5, ngram(2, getWords("big-seg.txt")))
	print frequencyTop(5, ngram(5, getWords("big-seg.txt")))