from collections import Counter
import math
import codecs

K = 10
V = 10000

def getWords(filename):
	with codecs.open(filename, 'r', 'utf-8') as f:
		return f.read()

def ngram(n, words):
	if n == 1:
		return (word for word in words)
	elif n == 2:
		return (words[i:i+2] for i in xrange(len(words)-1))

def frequency(tokens):
	return dict(Counter(map(tuple, tokens)))

def countOfFrequency(frequencies):
	return dict(Counter(frequencies.itervalues()))

def rStar(r, n, count_of_freq):
	if r == 0:
		if n == 1:
			n0 = V - sum(count_of_freq.itervalues())
		else:
			n0 = V**2 - sum(count_of_freq.itervalues())
		return count_of_freq[1] / float(n0)
	elif r < K:
		return (r+1) * count_of_freq[r+1] / float(count_of_freq[r])
	else:
		return r

def prob(N, rStars, r):
	return rStars[r]/float(N) if r < K else r/float(N)

def cond_prob(p2w, p1w):
	return p2w/float(p1w)

if __name__ == '__main__':
	
	import sys
	if len(sys.argv) < 2:
		exit()
	filename = sys.argv[1]
	words = getWords(filename)

	models_1 = frequency(ngram(1, words))
	count_of_freq_1 = countOfFrequency(models_1)
	rStars_1 = [rStar(r, 1, count_of_freq_1) for r in range(10)]
	Nk_1 = sum([i*count_of_freq_1[i] for i in count_of_freq_1.iterkeys()]) + K * count_of_freq_1[K-1]

	models_2 = frequency(ngram(2, words))
	count_of_freq_2 = countOfFrequency(models_2)
	rStars_2 = [rStar(r, 2, count_of_freq_2) for r in range(10)]
	Nk_2 = sum([i*count_of_freq_2[i] for i in count_of_freq_2.iterkeys()]) + K * count_of_freq_2[K-1]
	
	import pickle
	with open('lang_model','wb') as f:
		pickle.dump((models_1, models_2, (rStars_1, rStars_2), Nk_1), f)
	
