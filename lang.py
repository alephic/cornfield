from util import multidict_add
import vocab

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

def tag(t):
  return lambda tok: isinstance(tok, t)

def tag_head(t, h):
  return lambda tok: isinstance(tok, t) and tok.head == h

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

def parse_tokens(tokenss):
  fringe = tokenss
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

def get_adj_tag(head):
  return RLam(
    lambda tok:
      NP(tok.count, [AdjQual(head)]+tok.qualifiers) if isinstance(tok, NP) else None)

def get_noun_tag(head, plur=False):
  return NP(PLUR if plur else SING, [NounQual(head)])

def get_prep_tag(head):
  return RLam(lambda tok: PP(head, tok) if isinstance(tok, DP) else None)

def get_prep_mod_tag(head):
  return RLam(lambda tok1:
    LLam(lambda tok2:
      NP(tok2.count, [PrepQual(head, tok1)]+tok2.qualifiers) \
        if isinstance(tok2, NP) else None) \
      if isinstance(tok1, DP) else None)

def get_verb_tag(head, *arg_preds):
  def f(args, preds):
    if len(preds) == 0:
      return VP(head, args)
    return RLam(lambda tok: f(args+[tok], preds[1:]) if preds[0](tok) else None)
  return f([], arg_preds)

def get_det_tag(head, deft, count):
  return RLam(lambda tok:
    DP(head, deft, count, tok.qualifiers) \
      if isinstance(tok, NP) and tok.count == count else None)

known_tags = {}

def add_verb(head, *arg_preds):
  multidict_add(known_tags, head, get_verb_tag(head, *arg_preds))
def add_noun(head):
  multidict_add(known_tags, head, get_noun_tag(head))
def add_plur_noun(head):
  multidict_add(known_tags, head, get_noun_tag(head, plur=True))
def add_adj(head):
  multidict_add(known_tags, head, get_adj_tag(head))
def add_prep(head):
  multidict_add(known_tags, head, get_prep_tag(head))
def add_prep_mod(head):
  multidict_add(known_tags, head, get_prep_mod_tag(head))
def add_adv(head):
  multidict_add(known_tags, head, AdvP(head))
def add_det(head, deft, count):
  multidict_add(known_tags, head, get_det_tag(head, deft, count))

add_det('the', DEF, SING)
add_det('the', DEF, PLUR)
add_det('a', INDEF, SING)
add_det('an', INDEF, SING)
add_det('some', INDEF, PLUR)
add_prep('at')
add_prep('to')
add_prep('with')
add_prep('in')
add_prep('on')
add_prep('above')
add_prep('below')
add_prep_mod('of')
add_prep_mod('with')
add_adv('around')
add_adv('back')
add_adv('carefully')
add_adv('closely')
add_verb('look', tag_head(PP, 'at'))
add_verb('look', tag_head(AdvP, 'closely'), tag_head(PP, 'at'))
add_verb('look', tag_head(AdvP, 'around'))
add_verb('look', tag_head(AdvP, 'around'), tag_head(AdvP, 'carefully'))
add_verb('examine', tag(DP))
add_verb('go', tag_head(PP, 'to'))
add_verb('go', tag_head(AdvP, 'back'))
add_verb('put', tag(DP), tag_head(PP, 'on'))
add_verb('give', tag(DP), tag(DP))
add_verb('give', tag(DP), tag_head(PP, 'to'))
add_verb('open', tag(DP))
add_verb('open', tag(DP), tag_head(PP, 'with'))
add_verb('close', tag(DP))
add_verb('throw', tag(DP), tag_head(PP, 'at'))
for noun in vocab.nouns_auto:
  add_noun(noun)
  add_plur_noun(vocab.pluralize(noun))
for (noun, plur_noun) in vocab.nouns_infl:
  add_noun(noun)
  add_plur_noun(plur_noun)
for adj in vocab.adjectives:
  add_adj(color)

def guess_tags(word):
  res = [
    get_adj_tag(word),
    NP(PLUR if word.endswith('s') else SING, [NounQual(word)])
  ]
  return res

def get_tags(word):
  return known_tags[word] if word in known_tags else guess_tags(word)

def tokenize(text):
  words = text.lower().split(' ')
  tokenss = [[]]
  for word in words:
    tokenss = [tokens+[tag] for tokens in tokenss for tag in get_tags(word)]
  return tokenss

def parse_text(text):
  tokenss = tokenize(text)
  return parse_tokens(tokenss)
