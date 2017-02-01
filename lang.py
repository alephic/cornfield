from tags import *
from vocab import *

def lam_apply(tok1, tok2):
  y1 = tok1.rlam(tok1, tok2)
  if y1:
    yield y1
  y2 = tok2.llam(tok2, tok1)
  if y2:
    yield y2

def parse_tokens(tokenss):
  fringe = tokenss
  while True:
    if fringe == []:
      return
    curr = fringe.pop()
    if len(curr) == 1:
      yield curr[0]
    for i in range(len(curr)-1):
      if curr[i+1].bilam and i+2 < len(curr):
        res = curr[i+1].bilam(curr[i+1], curr[i], curr[i+2])
        if res:
          fringe.append(curr[:i]+[res]+curr[i+3:])
      for y in lam_apply(curr[i], curr[i+1]):
        fringe.append(curr[:i]+[y]+curr[i+2:])

def tokenize(text):
  res = []
  for chunk in text.split(' '):
    has_pf = False
    for pf in postfixes:
      if chunk.endswith(pf):
        res.append(chunk[:-len(pf)])
        res.append(pf)
        has_pf = True
        break
    if not has_pf:
      res.append(chunk)
  return res

def tag(text):
  words = tokenize(text)
  tokenss = [[]]
  for word in words:
    tokenss = [tokens+[tag] for tokens in tokenss for tag in get_tags(word.lower())]
  return tokenss

def parse_text(text):
  return next(parse_tokens(tag(text)), None)
