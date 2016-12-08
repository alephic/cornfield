from util import multidict_add
import vocab

class N:
  visible = True
  def __init__(self, head):
    self.head = head
  def __str__(self):
    return self.head
  def __repr__(self):
    return 'N.'+self.head
class Gender:
  visible = False
  def __init__(self, gender):
    self.gender = gender
  def __repr__(self):
    return {MASC:'MASC',FEM:'FEM',NEUT:'NEUT'}[self.gender]

#Gender values
MASC = object()
FEM = object()
NEUT = object()

#Count values
SING = object()
PLUR = object()

#Deft values
DEF = object()
INDEF = object()

class ArgBox:
  def __init__(self, boxed, extra=False):
    self.boxed = boxed
    self.extra = extra

class Tag:
  pass
class VP(Tag):
  def __init__(self, head, args):
    self.head = head
    self.args = args
  def __str__(self):
    return self.head+' '+' '.join(str(arg.boxed) for arg in self.args)
  def __repr__(self):
    return 'VP.'+self.head+'('+', '.join(repr(arg.boxed) for arg in self.args)+')'
class NP(Tag):
  def __init__(self, count, qualifiers):
    self.count = count
    self.qualifiers = qualifiers
  def __str__(self):
    return ' '.join(str(qual) for qual in self.qualifiers if qual.visible)
  def __repr__(self):
    return 'NP('+', '.join(repr(qual) for qual in self.qualifiers)+')'
class DP(Tag):
  def __init__(self, head, deft, count, qualifiers):
    self.head = head
    self.deft = deft
    self.count = count
    self.qualifiers = qualifiers
  def __str__(self):
    return self.head + ' ' + \
      ' '.join(str(qual) for qual in self.qualifiers if qual.visible)
  def __repr__(self):
    return 'DP.'+self.head+'('+', '.join(repr(qual) for qual in self.qualifiers)+')'
class PP(Tag):
  visible = True
  def __init__(self, head, arg):
    self.head = head
    self.arg = arg
  def __str__(self):
    return self.head + ' ' + str(self.arg) if self.arg else self.head
  def __repr__(self):
    return 'PP.'+self.head+'('+repr(self.arg)+')' if self.arg else 'PP.'+self.head
class RLam(Tag):
  def app(self, tok):
    return None
class LLam(Tag):
  def app(self, tok):
    return None
class RLamF(RLam):
  def __init__(self, f):
    self.f = f
  def app(self, tok):
    return self.f(tok)
  def __repr__(self):
    return 'RLamF'
class LLamF(LLam):
  def __init__(self, f):
    self.f = f
  def app(self, tok):
    return self.f(tok)
  def __repr__(self):
    return 'LLamF'
class Adj(RLam):
  visible = True
  def __init__(self, head):
    self.head = head
  def app(self, tok):
    return NP(tok.count, [self]+tok.qualifiers) \
      if isinstance(tok, NP) else None
  def __str__(self):
    return self.head
  def __repr__(self):
    return 'Adj.'+self.head
class V(RLam):
  def __init__(self, head, args, arg_preds):
    self.head = head
    self.args = args
    self.arg_preds = arg_preds
  def app(self, tok):
    if self.arg_preds[0](tok):
      if len(self.arg_preds) == 1:
        return VP(self.head, self.args+[ArgBox(tok)])
      else:
        return V(self.head, self.args+[ArgBox(tok)], self.arg_preds[1:])
    else:
      return None
  def __str__(self):
    return self.head+' '+' '.join(str(arg.boxed) for arg in self.args)
  def __repr__(self):
    return 'V.'+self.head+'('+', '.join(repr(arg.boxed) for arg in self.args)+', ' \
      +', '.join('?' for arg_pred in self.arg_preds)+')'
class Adv(LLam):
  def __init__(self, head):
    self.head = head
  def app(self, tok):
    if isinstance(tok, V):
      return V(tok.head, tok.args+[ArgBox(self, extra=True)], tok.arg_preds)
    elif isinstance(tok, VP):
      return VP(tok.head, tok.args+[ArgBox(self, extra=True)])
    else:
      return None
  def __str__(self):
    return self.head
  def __repr__(self):
    return 'Adv.'+self.head
class P(RLam):
  def __init__(self, head):
    self.head = head
  def app(self, tok):
    return PP(self.head, tok) if isinstance(tok, DP) else None
  def __str__(self):
    return self.head
  def __repr__(self):
    return 'P.'+self.head
class PM(RLam):
  def __init__(self, head):
    self.head = head
  def app(self, tok1):
    return LLamF(lambda tok2:
      NP(tok2.count, tok2.qualifiers+[PP(self.head, tok1)]) \
        if isinstance(tok2, NP) else None) \
      if isinstance(tok1, DP) else None
  def __str__(self):
    return self.head
  def __repr__(self):
    return 'PM.'+self.head
class D(RLam):
  def __init__(self, head, deft, count):
    self.head = head
    self.deft = deft
    self.count = count
  def app(self, tok):
    return DP(self.head, self.deft, self.count, tok.qualifiers) \
      if isinstance(tok, NP) and tok.count == self.count else None
  def __str__(self):
    return self.head
  def __repr__(self):
    return 'D.'+self.head

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

known_tags = {}

def add_verb(head, *arg_preds):
  multidict_add(known_tags, head, V(head, [], arg_preds))
def add_noun(head):
  multidict_add(known_tags, head, NP(SING, [Noun(head)]))
def add_plur_noun(head):
  multidict_add(known_tags, head, NP(PLUR, [Noun(head)]))
def add_adj(head):
  multidict_add(known_tags, head, AdjP(head))
def add_prep(head):
  multidict_add(known_tags, head, P(head))
def add_pp(head):
  multidict_add(known_tags, head, PP(head, None))
def add_prep_mod(head):
  multidict_add(known_tags, head, PM(head))
def add_adv(head):
  multidict_add(known_tags, head, Adv(head))
def add_det(head, deft, count):
  multidict_add(known_tags, head, D(head, deft, count))
def add_dp(head, deft, count, qualifiers):
  multidict_add(known_tags, head, DP(head, deft, count, qualifiers))

add_det('the', DEF, SING)
add_det('the', DEF, PLUR)
add_det('a', INDEF, SING)
add_det('an', INDEF, SING)
add_det('some', INDEF, PLUR)
add_dp('him', DEF, SING, [Gender(MASC)])
add_dp('her', DEF, SING, [Gender(FEM)])
add_dp('it', DEF, SING, [Gender(NEUT)])
add_dp('them', DEF, PLUR, [])
add_prep('at')
add_prep('to')
add_prep('with')
add_prep('in')
add_prep('on')
add_prep('above')
add_prep('below')
add_pp('back')
add_prep_mod('of')
add_prep_mod('with')
add_adv('around')
add_adv('back')
add_adv('carefully')
add_adv('closely')
add_verb('look', tag_head(PP, 'at'))
add_verb('look')
add_verb('examine', tag(DP))
add_verb('go', tag_head(PP, 'to'))
add_verb('go', tag_head(PP, 'back'))
add_verb('put', tag(DP), tag_head(PP, 'on'))
add_verb('give', tag(DP), tag(DP))
add_verb('give', tag(DP), tag_head(PP, 'to'))
add_verb('open', tag(DP))
add_verb('open', tag(DP), tag_head(PP, 'with'))
add_verb('close', tag(DP))
add_verb('throw', tag(DP), tag_head(PP, 'at'))
for noun in vocab.nouns:
  add_noun(noun)
  add_plur_noun(vocab.get_plural(noun))
for adj in vocab.adjs:
  add_adj(adj)

def guess_tags(word):
  res = [
    get_adj_tag(word),
    NP(PLUR if word.endswith('s') else SING, [Noun(word)])
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
