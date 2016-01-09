import random
import string
# refs:
# http://eflorenzano.com/blog/2008/11/17/writing-markov-chain-irc-bot-twisted-and-python/
# http://www.ccel.org/ccel/bible/kjv.txt

END = "END"


class Markov(object):

    """docstring for Markov"""

    def __init__(self, corpus, chain_len):
        self.corpus = []
        self.flat_corpus = ""
        self.markov = {}
        self.chain_len = chain_len

        for s in corpus:
            self.feed(s)

    def feed(self, msg):
        def add(key, val):
            self.markov.setdefault(key, []).append(val)
        self.corpus += msg
        self.flat_corpus += "".join(msg)

        buf = []
        for word in msg:
            add(tuple(buf), word)
            buf.append(word)
            if len(buf) > self.chain_len:
                del buf[0]
        add(tuple(buf), END)

    def generate(self, max_words=100):
        out = []
        buf = []
        for i in xrange(max_words):
            next_word = random.choice(self.markov[tuple(buf)])
            # print "B", buf
            # print "C", len(markov[tuple(buf)])
            # print "M", markov[tuple(buf)]
            # print
            if next_word == END:
                break
            buf.append(next_word)
            if len(buf) > self.chain_len:
                del buf[0]
            out.append(next_word)
        return out

    def generate_original(self, max_words=100):
        for i in range(100):
            s = self.generate(max_words)
            if not self.is_in_corpus(s):
                return s

    def is_in_corpus(self, words):
        sub = "".join(words)
        return string.find(self.flat_corpus, sub) != -1

    def get_prob(self, words):
        words = list(words)
        words.reverse()
        buf = []
        den = num = 1.
        while len(words):
            next_word = words.pop()
            den *= len([True for w in self.markov[tuple(buf)] if w is next_word])
            num *= len(self.markov[tuple(buf)])

            buf.append(next_word)
            if len(buf) > self.chain_len:
                del buf[0]
        return den / num


def get_sentence(filename):
    """given filename, yield santised sentences as word list"""

    words = []
    with open(filename) as corp:
        for l in corp:
            l = l.translate(None, "\"#$%&'()*+,-/:;<=>@[\\]^_`{|}~'")
            words += l.strip().lower().split()
    words.reverse()
    buf = []
    while len(words):
        buf.append(words.pop())
        if buf[-1].endswith(".")\
                or buf[-1].endswith("?")\
                or buf[-1].endswith("!"):
            yield buf
            buf = []

import itertools

syms = lambda a,b: len([x for x,y in zip(reversed(a),reversed(b)) if x == y])
rhymes = lambda a,b: len([x for x,y in itertools.takewhile(lambda x: x[0] == x[1], itertools.izip(reversed(a),reversed(b)))])

import phonetics
import sys

from nltk.corpus import cmudict
p_dict = cmudict.dict()

vow = lambda line: [l for l in line if phonetics.is_vow(l)]
get_phon = lambda x: p_dict[x]
magic = lambda a1,b1: set(a + b for a,b in itertools.product(a1,b1))
magic_syl = lambda a1,b1: [a + [b] for a,b in itertools.product(a1,b1)]
syl = lambda word: [len(list(y for y in x if y[-1].isdigit())) for x in p_dict[word.lower()]]

if __name__ == '__main__':
    # my_little_markov = Markov(get_sentence("bible.txt"), 2)
    my_little_markov = Markov(get_sentence("jimstone.txt"), 2)
    # my_little_markov = Markov(get_sentence("timecube.txt"), 2)
    # my_little_markov = Markov(get_sentence("scientology.txt"), 2)
    def gen():
        while 1:
            try:
                x = my_little_markov.generate_original()
                p = [k[-3:] for k in get_phon(x[-1].strip('?!.'))]
#                reduce(magic_syl, [get_phon(w.strip('?!.')) for w in x], [[]])
                s = reduce(magic, [syl(w.strip('?!.')) for w in x])
                yield ( x, #raw
                        p, #phon
                        s
                    )
            except KeyError as e:
                pass
    line_lens = {}
    longer = False
    shorter = False
    for line in gen():
        for length in line[2]:
            for rime in line[1]:
                cur = line_lens.setdefault(length, {}).setdefault(tuple(rime), [])
                if any(line[0][-1].strip('?!.;') == prev[0][-1].strip('?!;.') for prev in cur):
                    continue
                line[0][-1] = line[0][-1][:-1] + ';'
                cur.append(line)
                if length == 9 and len(cur) >= 3:
                    longer = cur
                if length == 6 and len(cur) >= 2:
                    shorter = cur
                if shorter and longer:
                    print ' '.join(longer[0][0])
                    print ' '.join(longer[1][0])
                    print ' '.join(shorter[0][0])
                    print ' '.join(shorter[1][0])
                    print ' '.join(longer[2][0])

                    exit()
                    raw_input()
                    longer = False
                    shorter = False
                    line_lens = {}
                    
