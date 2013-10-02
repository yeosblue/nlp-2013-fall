def ngram(n, words):
	return (words[i:i+n] for i in xrange(len(words)-n+1))

def getWords(filename):
    with open(filename) as f:
    	return f.read().split()

def frequencyTop(top_n, words):
    from collections import Counter
    return Counter(map(tuple, words)).most_common(top_n)

if __name__ == "__main__":

    for i in reversed(range(1, 6)):
        print frequencyTop(5, ngram(i, getWords("big-seg.txt")))
