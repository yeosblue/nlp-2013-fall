from collections import Counter
import math

K = 10
V = 80000

def getWords(filename):
	with open(filename) as f:
		return f.read().split()

def ngram(n, words):
	return (words[i:i+n] for i in xrange(len(words)-n+1))

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
	
	words = getWords('VOA.txt')

	models_1 = frequency(ngram(1, words))
	count_of_freq_1 = countOfFrequency(models_1)
	rStars_1 = [rStar(r, 1, count_of_freq_1) for r in range(10)]
	Nk_1 = sum([i*count_of_freq_1[i] for i in count_of_freq_1.iterkeys()]) + K * count_of_freq_1[K]

	models_2 = frequency(ngram(2, words))
	count_of_freq_2 = countOfFrequency(models_2)
	rStars_2 = [rStar(r, 2, count_of_freq_2) for r in range(10)]
	Nk_2 = sum([i*count_of_freq_2[i] for i in count_of_freq_2.iterkeys()]) + K * count_of_freq_2[K]
	
	from functools import partial
	prob_1 = partial(prob, Nk_1, rStars_1)
	prob_2 = partial(prob, Nk_2, rStars_2)

	# --- test case 1 ---
	test = 'this is a book'
	print test
	tokens_1 = map(tuple, ngram(1, test.split()))
	tokens_2 = map(tuple, ngram(2, test.split()))

	long_tail = [cond_prob(prob_2(models_2.get(tokens_2[i], 0)), prob_1(models_1.get(tokens_1[i], 0))) for i in range(len(tokens_2))]
	print math.log10(prob_1(models_1.get(tokens_1[0], 0))) + sum(map(math.log10, long_tail))
	
	# --- test case 2 ---
	test = 'this is an book'
	print test
	tokens_1 = map(tuple, ngram(1, test.split()))
	tokens_2 = map(tuple, ngram(2, test.split()))

	long_tail = [cond_prob(prob_2(models_2.get(tokens_2[i], 0)), prob_1(models_1.get(tokens_1[i], 0))) for i in range(len(tokens_2))]
	print math.log10(prob_1(models_1.get(tokens_1[0], 0))) + sum(map(math.log10, long_tail))


