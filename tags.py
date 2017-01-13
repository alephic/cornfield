
# Person
PERSON = object()
FIRST = object()
SECOND = object()
THIRD = object()

# Case
CASE = object()
NOM = object()
ACC = object()

# Count
COUNT = object()
SING = object()
PLUR = object()

# Verb tense/aspect
FORM = object()
BASE = object()
PRET = object()
PRES = object()
PART = object()
GERUND = object()

# Span labels
CAT = object()
N = object()
NP = object()
DP = object()
V = object()
VP = object()
TP = object()
CP = object()
Adj = object()
Adv = object()
PP = object()

# Special values
ANY = object()

# Special features
HAS_SUBJ = object()
PP_LEX = object()

def matches(spec, feat):
  if spec == ANY or feat == ANY:
    return True
  if isinstance(feat, list):
    if isinstance(spec, list):
      for f in feat:
        if f in spec:
          return True
    return spec in feat
  elif isinstance(spec, list):
    return feat in spec
  return feat == spec

def pat_matches(pat, tok):
  if isinstance(pat, list):
    for subpat in pat:
      m = True
      for (f, s) in subpat.items():
        if not matches(s, tok[f]):
          m = False
          break
      if m:
        return True
    return False
  else:
    for (f, s) in pat.items():
      if not matches(s, tok[f]):
        return False
    return True

def no_lam(token, other):
  pass

class Token:
  def __init__(self, lex, rlam=no_lam, llam=no_lam):
    self.lex = lex
    self.rlam = rlam
    self.llam = llam
  def __getitem__(self, item):
    pass
  def __str__(self):
    return self.lex

class FeatToken(Token):
  def __init__(self, lex, feats, rlam=no_lam, llam=no_lam):
    super().__init__(lex, rlam=rlam, llam=llam)
    self.feats = feats
  def __getitem__(self, item):
    return self.feats[item] if item in self.feats else None
    
class HeadedToken(Token):
  def __getitem__(self, item):
    return self.head[item]

class Arg(HeadedToken):
  def __init__(self, head, arg, rlam=no_lam, llam=no_lam, feats={}):
    self.head = head
    self.arg = arg
    self.rlam = rlam
    self.llam = llam
    self.feats = feats
  def __getitem__(self, item):
    return self.feats[item] if item in self.feats else self.head[item]

class ArgR(Arg):
  def __str__(self):
    return str(self.head)+' '+str(self.arg)

class ArgL(Arg):
  def __str__(self):
    return str(self.arg)+' '+str(self.head)
    
def mod_rlam(mod, other):
  res = mod.head.rlam(mod.head, other)
  if res and isinstance(res, Arg) and res.head == mod.head:
    res.head = mod
  return res
def mod_llam(mod, other):
  res = mod.head.llam(mod.head, other)
  if res and isinstance(res, Arg) and res.head == mod.head:
    res.head = mod
  return res

class Mod(HeadedToken):
  def __init__(self, head, mod):
    self.head = head
    self.mod = mod
    self.rlam = mod_rlam
    self.llam = mod_llam

class ModR(Mod):
  def __str__(self):
    return str(self.head)+' '+str(self.mod)

class ModL(Mod):
  def __str__(self):
    return str(self.mod)+' '+str(self.head)

def get_verb_rlam(arg_pats):
  if len(arg_pats) == 0:
    return no_lam
  def verb_rlam(vp, other):
    if pat_matches(arg_pats[0], other):
      return ArgR(vp, other, rlam=get_verb_rlam(arg_pats[1:]), llam=vp.llam)
  return verb_rlam
def verb_llam(vp, other):
  if pat_matches({CAT: DP, CASE: NOM, PERSON: vp[PERSON], COUNT: vp[COUNT]}, other):
    return ArgL(vp, other, rlam=vp.rlam, feats={HAS_SUBJ:True})

class Verb(FeatToken):
  def __init__(self, lex, form, subj_person, subj_count, arg_pats):
    self.lex = lex
    self.feats = {FORM: form, CAT: VP, PERSON: subj_person, COUNT: subj_count}
    self.rlam = get_verb_rlam(arg_pats)
    self.llam = verb_llam

class Noun(FeatToken):
  def __init__(self, lex, count):
    if count == PLUR:
      fs = {CAT: [NP, DP], COUNT: PLUR, CASE: ANY, PERSON: THIRD}
    else:
      fs = {CAT: NP, COUNT: SING}
    super().__init__(lex, fs)

def pos_adj_rlam(adj, other):
  if matches(NP, other[CAT]):
    return ModL(other, adj)

class PosAdjective(FeatToken):
  def __init__(self, lex):
    super().__init__(lex, {CAT: Adj}, rlam=pos_adj_rlam)

def det_rlam(det, other):
  if pat_matches({CAT: NP, COUNT: det[COUNT]}, other):
    return ArgR(det, other, feats={CAT: DP, PERSON: THIRD, CASE: ANY})

class Determiner(FeatToken):
  def __init__(self, lex, count):
    super().__init__(lex, {COUNT: count}, rlam=det_rlam)

def adv_rlam(adv, other):
  if matches(VP, other[CAT]):
    return ModL(other, adv)
def adv_llam(adv, other):
  if matches(VP, other[CAT]):
    return ModR(other, adv)

class Adverb(FeatToken):
  def __init__(self, lex):
    super().__init__(lex, {CAT: Adv}, rlam=adv_rlam, llam=adv_llam)

def get_prep_rlam(head_pat, arg_pat):
  def prep_llam(prep, other):
    if pat_matches(head_pat, other):
      return ModR(other, prep)
  def prep_rlam(prep, other):
    if pat_matches(arg_pat, other):
      return ArgR(prep, other, feats={CAT:PP}, llam=prep_llam)
  return prep_rlam

class Preposition(FeatToken):
  def __init__(self, lex, head_pat, arg_pat):
    super().__init__(lex, {PP_LEX: lex}, rlam=get_prep_rlam(head_pat, arg_pat))
  