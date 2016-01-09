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
vow = lambda line: [l for l in line if phonetics.is_vow(l)]
syl = lambda line: len([l for l in line if phonetics.is_vow(l)])

if __name__ == '__main__':
    my_little_markov = Markov(get_sentence("bible.txt"), 2)
    # my_little_markov = Markov(get_sentence("jimstone.txt"), 3)
    # my_little_markov = Markov(get_sentence("timecube.txt"), 3)
    # my_little_markov = Markov(get_sentence("scientology.txt"), 3)
    def gen():
        while 1:
            x = my_little_markov.generate_original()
            p = phonetics.get_phonetic_transcription(' '.join(x))
            yield (x, #raw
                p, #phon
                vow(p), #vows
                syl(p)) #syllas 
    line_lens = {}
    longer = False
    shorter = False
    for line in gen():
        cur = line_lens.setdefault(line[3], {}).setdefault(line[2][-1], [])
        cur.append(line)
        if line[3] == 8 and len(cur) >= 3:
            longer = cur
        if line[3] == 6 and len(cur) >= 2:
            shorter = cur
        if shorter and longer:
            break

    print longer[0][0]
    print longer[1][0]
    print shorter[0][0]
    print shorter[1][0]
    print longer[2][0]

    print longer[0]
    print longer[1]
    print shorter[0]
    print shorter[1]
    print longer[2]





