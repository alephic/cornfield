
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
      for (s, f) in subpat.items():
        if not matches(s, tok[f]):
          m = False
          break
      if m:
        return True
    return False
  else:
    for (s, f) in pat.items():
      if not matches(s, tok[f]):
        return False
    return True

class Token:
  def __init__(self, lex):
    self.lex = lex
  def __getitem__(self, item):
    pass
  def __str__(self):
    return self.lex
  def rlam(self, other):
    pass
  def llam(self, other):
    pass

class FeatToken(Token):
  def __init__(self, lex, feats, rlam=Token.rlam, llam=Token.llam):
    self.lex = lex
    self.feats = feats
    self.rlam = rlam
    self.llam = llam
  def __getitem__(self, item):
    return self.feats[item] if item in self.feats else None
    
class HeadedToken(Token):
  def __getitem__(self, item):
    return self.head[item]

class Arg(HeadedToken):
  def __init__(self, head, arg, rlam=Token.rlam, llam=Token.llam, feats={}):
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

class Mod(HeadedToken):
  def __init__(self, head, mod):
    self.head = head
    self.mod = mod
  def rlam(self, other):
    res = self.head.rlam(other)
    if res and isinstance(res, Arg):
      res.head = self
    return res
  def llam(self, other):
    res = self.head.llam(other)
    if res and isinstance(res, Arg):
      res.head = self
    return res

class ModR(Mod):
  def __str__(self):
    return str(self.head)+' '+str(self.mod)

class ModL(Mod):
  def __str__(self):
    return str(self.mod)+' '+str(self.head)

def get_verb_rlam(arg_pats):
  if len(arg_pats) == 0:
    return Token.rlam
  class Dummy:
    def rl(self, other):
      if pat_matches(arg_pats[0], other):
        return ArgR(self, other, rlam=get_verb_rlam(arg_pats[1:]), llam=self.llam)
  return Dummy.rl

class Verb(FeatToken):
  def __init__(self, lex, form, subj_person, subj_count, arg_pats):
    self.lex = lex
    self.feats = {FORM: form, CAT: VP, PERSON: subj_person, COUNT: subj_count}
    self.rlam = get_verb_rlam(arg_pats)
  def llam(self, other):
    if pat_matches({CAT: DP, CASE: NOM, PERSON: self[PERSON], COUNT: self[COUNT]}, other):
      return ArgL(self, other, rlam=self.rlam, feats={HAS_SUBJ:True})

class Noun(FeatToken):
  def __init__(self, lex, count):
    self.lex = lex
    if count == PLUR:
      self.feats = {CAT: [NP, DP], COUNT: PLUR, CASE: ANY, PERSON: THIRD}
    else:
      self.feats = {CAT: NP, COUNT: SING}

class PosAdjective(FeatToken):
  def __init__(self, lex):
    self.lex = lex
    self.feats = {CAT: Adj}
  def rlam(self, other):
    if matches(NP, other[CAT]):
      return ModL(other, self)
  
class Determiner(FeatToken):
  def __init__(self, lex, count):
    self.lex = lex
    self.feats = {COUNT: count}
  def rlam(self, other):
    if pat_matches({CAT: NP, COUNT: self[COUNT]}, other):
      return ArgR(self, other, feats={CAT: DP, PERSON: THIRD, CASE: ANY})

class Adverb(FeatToken):
  def __init__(self, lex):
    self.lex = lex
    self.feats = {CAT: Adv}
  def rlam(self, other):
    if matches(VP, other[CAT]):
      return ModL(other, self)
  def llam(self, other):
    if matches(VP, other[CAT]):
      return ModR(other, self)

def get_prep_rlam(head_pat, arg_pat):
  class Dummy:
    def llam(self, other):
      if pat_matches(head_pat, other):
        return ModR(other, self)
    def rlam(self, other):
      if pat_matches(arg_pat, other):
        return ArgR(self, other, feats={CAT:PP}, llam=Dummy.llam)
  return Dummy.rlam

class Preposition(FeatToken):
  def __init__(self, lex, head_pat, arg_pat):
    self.lex = lex
    self.feats = {PP_LEX: lex}
    self.rlam = get_prep_rlam(head_pat, arg_pat)
  