import re
import random

from util import hook

special = ['ripuli', 'memes', 'death']

@hook.command
def choose(inp):
    ".choose <choice1>, <choice2>, ... <choicen> -- makes a decision"

    c = re.findall(r'([^,]+)', inp)
    if len(c) == 1:
        c = re.findall(r'(\S+)', inp)
        if len(c) == 1:
            return 'the decision is up to you'
    for word in special:
        if word in c:
            return word
    return random.choice(c).strip()
