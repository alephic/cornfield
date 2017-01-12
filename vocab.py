from util import multidict_add
from tags import *

known_tags = {}

def add_tok(tok):
  multidict_add(known_tags, tok.lex, tok)

add_tok(Determiner('the', [SING, PLUR]))
add_tok(Determiner('a', SING))
add_tok(FeatToken('i', {CAT:DP, CASE:NOM, COUNT:SING, PERSON:FIRST}))
add_tok(FeatToken('we', {CAT:DP, CASE:NOM, COUNT:PLUR, PERSON:FIRST}))

def guess_tags(lex):
  if tok.endswith('s'):
    return FeatToken(lex, {CAT:[NP, DP], CASE:[NOM, ACC] COUNT:PLUR})
  return FeatToken(lex, {CAT:NP, COUNT:SING})