from .markov import Markov

import sys
import os

from willie.module import commands


@commands('markov')
def markov_excrete(bot, trigger):
    ret = bot.memory['markov'].generate_original(30)
    bot.say(" ".join(ret))

@commands('markov2')
def markov_feed(bot, trigger):
    bot.memory['markov'].feed(trigger.group().split())


def setup(bot):
    bot.memory['markov'] = Markov(["yo", "dawg"], 3)

if __name__ == '__main__':
    print 'yep'
