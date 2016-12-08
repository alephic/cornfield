
class NounQual:
  def __init__(self, head):
    self.head = head

class AdjQual:
  def __init__(self, head):
    self.head = head

class PrepQual:
  def __init__(self, prep_head, arg):
    self.prep_head = prep_head
    self.arg = arg

#Count values
SING = object()
PLUR = object()

#Deft values
DEF = object()
INDEF = object()

class Tag:
  pass
class VP(Tag):
  def __init__(self, head, args):
    self.head = head
    self.args = args
class NP(Tag):
  def __init__(self, count, qualifiers):
    self.count = count
    self.qualifiers = qualifiers
class DP(Tag):
  def __init__(self, head, deft, count, qualifiers):
    self.head = head
    self.deft = deft
    self.count = count
    self.qualifiers = qualifiers
class PP(Tag):
  def __init__(self, head, arg):
    self.head = head
    self.arg = arg
class AdvP(Tag):
  def __init__(self, head):
    self.head = head
class RLam(Tag):
  def __init__(self, app):
    self.app = app
class LLam(Tag):
  def __init__(self, app):
    self.app = app

def has_tag(t):
  return lambda tok: isinstance(tok, t)

def get_adj_tag(head):
  return RLam(
    lambda tok:
      NP([AdjQual(head)]+tok.qualifiers) if isinstance(tok, NP) else None)

def get_prep_tag(head):
  return RLam(lambda tok: PP(head, tok) if isinstance(tok, DP) else None)

def get_verb_tag(head, *arg_preds):
  if len(arg_preds) == 0:
    return VP(head, [])
  pred = arg_preds[0]
  rest = get_verb_tag(head, *arg_preds[1:])
  return lambda tok: rest if pred(tok) else None

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

def promote(tok):
  res = []
  if isinstance(tok, NP) and tok.count == PLUR:
    res.append(DP(None, INDEF, PLUR, tok.qualifiers))
  return res

def parse_tokens(tokens):
  fringe = [tokens]
  while True:
    if fringe == []:
      return None
    curr = fringe.pop()
    if len(curr) == 1:
      return curr[0]
    for i in range(len(curr)):
      if i < len(curr) - 1:
        for y in lam_apply(curr[i], curr[i+1]):
          fringe.append(curr[:i]+[y]+curr[i+2:])
      for y in promote(curr[i]):
        fringe.append(curr[:i]+[y]+curr[i+1:])

def parse_text(text):
  words = text.lower().split(' ')
  tokens = [(tags[w] if w in tags else guess_tags[w]) for w in words]
  return parse_tokens(tokens)
