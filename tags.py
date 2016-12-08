
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
