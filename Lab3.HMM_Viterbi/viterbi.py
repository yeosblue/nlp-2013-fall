# -*- coding: utf-8 -*- 
from collections import defaultdict
from itertools import chain, product

def print_dptable(V):
    print "   ",
    for i in range(len(V)):
        print "%7s" % ("%d" % i),
    print

    for y in V[0].keys():
        print "%.5s: " % y,
        for t in range(len(V)):
            print "%.7s" % ("%f" % V[t][y]),
        print

def viterbi(obs, states, start_p, trans_p, emit_p):
    V, path = [{}], {}

    for y in states:
        V[0][y], path[y] = start_p[y] * emit_p[y][obs[0]], [y]

    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max([(V[t-1][y0]*trans_p[y0][y]*emit_p[y][obs[t]], y0) for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath
    print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def getBPMF():
    import codecs
    with codecs.open('bpmf.txt', 'r', 'utf-8') as f:
        return [line.split() for line in f.readlines()]

if __name__ == '__main__':
    
    # run good_turing_zh to generate lang_model before this
    import pickle
    with open('lang_model') as f:
        uniDict, biDict, smooth, total = pickle.load(f)

    phonicDict = defaultdict(list)
    for line in getBPMF():
        phonicDict[line[0]] += line[2]

    obs = [u'ㄓ', u'ㄏ', u'ㄇ', u'ㄍ', u'ㄓ', u'ㄈ']
    states = list(chain(*[phonicDict[ob] for ob in obs])) # make it flat
    
    from good_turing_zh import prob, cond_prob
    from functools import partial
    prob_1, prob_2 = partial(prob, total, smooth[0]), partial(prob, total, smooth[1])    
    start_prob = {state:prob_1(uniDict.get(state, 0)) for state in states}
    
    transition_prob = defaultdict(dict)
    for former_state, latter_state in product(states, repeat=2):
        transition_prob[former_state][latter_state] = cond_prob(prob_2(biDict.get((former_state, latter_state), 0)), prob_1(uniDict.get(former_state, 0)))
    
    emission_prob = defaultdict(dict)
    for state, ob in product(states, obs):
        emission_prob[state][ob] = 1 if state in phonicDict[ob] else 0
    
    print viterbi(obs, states, start_prob, transition_prob, emission_prob)

