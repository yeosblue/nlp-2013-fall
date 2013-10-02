def ngram(n, words):
    for i in xrange(len(words)-n+1):
        yield words[i:i+n]

def getWords(filename):
    from itertools import chain
    with open(filename) as f:
    	return list(chain(*(line.split() for line in f.readlines())))

def frequencyTop(top_n, words):
    from collections import Counter
    return Counter(map(tuple, words)).most_common(top_n)

if __name__ == "__main__":

    for i in reversed(range(1, 6)):
        print frequencyTop(5, ngram(i, getWords("big-seg.txt")))
    