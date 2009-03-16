import hashlib

import hook

@hook.command
def md5(input):
    return hashlib.md5(input).hexdigest()

@hook.command
def sha1(input):
    return hashlib.sha1(input).hexdigest()

@hook.command
def hash(input):
    return ', '.join(x + ": " + getattr(hashlib, x)(input).hexdigest()
            for x in 'md5 sha1 sha256'.split())