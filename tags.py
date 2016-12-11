
class N:
  def __init__(self, head):
    self.head = head
  def __str__(self):
    return self.head
  def __repr__(self):
    return 'N.'+self.head
class Pronoun:
  def __init__(self, gender, reflexive=False):
    self.gender = gender
    self.reflexive = reflexive
  def __repr__(self):
    g = {MASC:'MASC',FEM:'FEM',NEUT:'NEUT'}[self.gender]
    return 'PRO.REFL.'+g if self.reflexive else 'PRO.'+g
class Speaker:
  def __repr__(self):
    return 'SPEAKER'
class Listener:
  def __repr__(self):
    return 'LISTENER'
class Possessive:
  def __init__(self, owner, owned):
    self.owner = owner
    self.owned = owned
  def __repr__(self):
    return 'POSS('+repr(self.owner)+','+repr(self.owned)+')'

#Gender values
MASC = object()
FEM = object()
NEUT = object()

#Count values
SING = object()
PLUR = object()
UNSPEC = object()

#Deft values
DEF = object()
INDEF = object()

#Form values
BASE = object() # have / eat
TPSINGPRES = object() # has / eats
PRET = object() # had / ate
PART = object() # had / eaten
GERUND = object() # having / eating
#Extra form values
FPSINGPRES = object() # am
PLURPRES = object() # are
SINGPRET = object() # was
PLURPRET = object() # were

def form_conflicts(f1, f2):
  if f1 == PRET and (f2 in (SINGPRET, PLURPRET)):
    return False
  if f2 == PRET and (f1 in (SINGPRET, PLURPRET)):
    return False
  if f1 == f2:
    return False
  return True

#Restrict values
OBJ = object()
SUBJ = object()

def subj_form_agrees(subj, form):
  ct = subj.count if isinstance(subj, DP) else PLUR
  ps = subj.person if isinstance(subj, DP) else 3
  if form == BASE:
    return ps != 3 or ct == PLUR
  elif form == TPSINGPRES:
    return ps == 3 and ct == SING
  elif form == PRET:
    return True
  elif form == SINGPRET:
    return ct == SING
  elif form == PLURPRET or form == PLURPRES:
    return ct == PLUR
  elif form == FPSINGPRES:
    return ps == 1 and ct == SING
  return False

def intern_arg(tok):
  return ((not tok.restrict) or (tok.restrict == OBJ)) if isinstance(tok, DP) else True

def extern_arg(tok):
  return ((not tok.restrict) or (tok.restrict == SUBJ)) if isinstance(tok, DP) else True

class ArgBox:
  def __init__(self, boxed, extra=False):
    self.boxed = boxed
    self.extra = extra

class Tag:
  head = None
class TP(Tag):
  def __init__(self, head, form, args):
    self.head = head
    self.form = form
    self.args = args
  def __str__(self):
    return str(self.args[0].boxed)+' '+self.head+' '+' '.join(str(arg.boxed) for arg in self.args)
  def __repr__(self):
    return 'TP.'+self.head+'('+', '.join(repr(arg.boxed) for arg in self.args)+')'
class NP(Tag):
  visible = True
  def __init__(self, count, qualifiers):
    self.count = count
    self.qualifiers = qualifiers
  def __str__(self):
    return ' '.join(str(qual) for qual in self.qualifiers)
  def __repr__(self):
    return 'NP('+', '.join(repr(qual) for qual in self.qualifiers)+')'
class DP(Tag):
  def __init__(self, head, deft, count, arg, restrict=None, person=3):
    self.head = head
    self.deft = deft
    self.count = count
    self.arg = arg
    self.restrict = restrict
    self.person = person
  def __str__(self):
    if isinstance(self.arg, NP):
      return self.head+' '+str(self.arg)
    elif isinstance(self.arg, Possessive):
      return str(self.arg.owner)+"'s "+str(self.arg.owned)
    return self.head
  def __repr__(self):
    return 'DP.'+self.head+'('+repr(self.arg)+')'
class ConjP(Tag):
  def __init__(self, head, args):
    self.head = head
    self.args = args
  def __str__(self):
    return ', '.join(str(arg) for arg in args[:-1])+' '+self.head+' ' \
      + str(self.args[-1])
  def __repr__(self):
    return 'ConjP.'+self.head+'('+', '.join(repr(arg) for arg in self.args)+')'
class PP(Tag):
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
  def __init__(self, head):
    self.head = head
  def app(self, tok):
    return NP(tok.count, [self]+tok.qualifiers) \
      if tag(tok, NP) else None
  def __str__(self):
    return self.head
  def __repr__(self):
    return 'Adj.'+self.head
class VP(LLam):
  def __init__(self, head, form, args):
    self.head = head
    self.form = form
    self.args = args
  def app(self, tok):
    if tag(tok, DP) and extern_arg(tok) and subj_form_agrees(tok, self.form):
      return TP(self.head, self.form, [ArgBox(tok)]+self.args)
    else:
      return None
  def __str__(self):
    return self.head+' '+' '.join(str(arg.boxed) for arg in self.args)
  def __repr__(self):
    return 'VP.'+self.head+'('+', '.join(repr(arg.boxed) for arg in self.args)+')'
class V(RLam):
  def __init__(self, head, form, args, arg_preds):
    self.head = head
    self.form = form
    self.args = args
    self.arg_preds = arg_preds
  def app(self, tok):
    if self.arg_preds[0](tok):
      if len(self.arg_preds) == 1:
        return VP(self.head, self.form, self.args+[ArgBox(tok)])
      else:
        return V(self.head, self.form, self.args+[ArgBox(tok)], self.arg_preds[1:])
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
    if tag(tok, V):
      return V(tok.head, tok.args+[ArgBox(self, extra=True)], tok.arg_preds)
    elif tag(tok, VP):
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
    return PP(self.head, tok) if tag(tok, DP) else None
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
        if tag(tok2, NP) else None) \
      if tag(tok1, DP) else None
  def __str__(self):
    return self.head
  def __repr__(self):
    return 'PM.'+self.head
class D(RLam):
  def __init__(self, head, deft, count, restrict, person):
    self.head = head
    self.deft = deft
    self.count = count
    self.restrict = restrict
    self.person = person
  def app(self, tok):
    return DP(self.head, self.deft, tok.count, tok, self.restrict, self.person) \
      if tag(tok, NP) and (tok.count == self.count or self.count == UNSPEC) else None
  def __str__(self):
    return self.head
  def __repr__(self):
    return 'D.'+self.head
class Conj(RLam):
  def __init__(self, head):
    self.head = head
  def app(self, tok1):
    def f(tok2):
      if tok1.__class__ == tok2.__class__:
        if tok1.__class__ in (V, VP) and form_conflicts(tok1.form, tok2.form):
          return None
        return ConjP(self.head, [tok2, tok1])
      return None
    return LLamF(f)

list_comma_tag = LLamF(lambda tok1:
  RLamF(lambda tok2: ConjP(tok2.head, [tok1]+tok2.args) if isinstance(tok2, ConjP) \
    and isinstance(tok2.args[0], tok1.__class__) else None))

poss_suff_tag = LLamF(lambda tok1:
  RLamF(lambda tok2:
    DP("'s", DEF, tok2.count, Possessive(tok1, tok2), None, 3) \
      if tag(tok2, NP) else None) \
    if tag(tok1, DP) else None)

def tag(tok, t):
  return isinstance(tok, t) or (isinstance(tok, ConjP) and isinstance(tok.args[0], t))

def tag_head(tok, t, h):
  if isinstance(tok, t) and tok.head == h:
    return True
  if isinstance(tok, ConjP):
    for arg in tok.args:
      if not (isinstance(tok, t) and tok.head == head):
        return False
    return True
  return False

def vp_form(tok, form):
  if isinstance(tok, VP) and tok.form == form:
    return True
  if isinstance(tok, ConjP):
    for arg in tok.args:
      if not (isinstance(tok, VP) and tok.form == form):
        return False
    return True
  return False

def tag_p(t):
  return lambda tok: tag(tok, t)
def tag_head_p(t, h):
  return lambda tok: tag_head(tok, t, h)
def vp_form_p(form):
  return lambda tok: vp_form(tok, form)

def pred_or(*preds):
  def f(t):
    for pred in preds:
      if pred(t):
        return True
    return False
  return f
