from tags import *
from vocab import *

def lam_apply(tok1, tok2):
  res = []
  if isinstance(tok1, RLam):
    y1 = tok1.app(tok2)
    if y1:
      res.append(y1)
  if isinstance(tok2, LLam):
    y2 = tok2.app(tok1)
    if y2:
      res.append(y2)
  return res

def parse_tokens(tokenss):
  fringe = tokenss
  while True:
    if fringe == []:
      return None
    curr = fringe.pop()
    if len(curr) == 1:
      return curr[0]
    for i in range(len(curr)-1):
      for y in lam_apply(curr[i], curr[i+1]):
        fringe.append(curr[:i]+[y]+curr[i+2:])

def tokenize(text):
  words = text.lower().split(' ')
  tokenss = [[]]
  for word in words:
    tokenss = [tokens+[tag] for tokens in tokenss for tag in get_tags(word)]
  return tokenss

def parse_text(text):
  tokenss = tokenize(text)
  return parse_tokens(tokenss)
