
class Feat:
  def __init__(self, name):
    self.name = name
  def __repr__(self):
    return self.name
  def __str__(self):
    return self.name

# Person
PERSON = Feat("PERSON")
FIRST = Feat("FIRST")
SECOND = Feat("SECOND")
THIRD = Feat("THIRD")

# Case
CASE = Feat("CASE")
NOM = Feat("NOM")
ACC = Feat("ACC")

# Count
COUNT = Feat("COUNT")
SING = Feat("SING")
PLUR = Feat("PLUR")

# Verb tense/aspect
FORM = Feat("FORM")
BARE = Feat("BARE")
PRET = Feat("PRET")
PRES = Feat("PRES")
PART = Feat("PART")
GERUND = Feat("GERUND")
MODAL = Feat("MODAL")
INF = Feat("INF")

# Span labels
CAT = Feat("CAT")
NP = Feat("NP")
DP = Feat("DP")
V = Feat("V")
VB = Feat("VB")
VP = Feat("VP")
TP = Feat("TP")
CP = Feat("CP")
Adj = Feat("Adj")
Adv = Feat("Adv")
PP = Feat("PP")

# Special values
ANY = Feat("ANY")

# Special features
HAS_SUBJ = Feat("HAS_SUBJ")
LEX = Feat("LEX")
ARG_CAT = Feat("ARG_CAT")

# Moods
MOOD = Feat("MOOD")
INTER = Feat("INTER")
DECL = Feat("DECL")

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
  def __repr__(self):
    return self.lex

class FeatToken(Token):
  def __init__(self, lex, feats, rlam=no_lam, llam=no_lam):
    super().__init__(lex, rlam=rlam, llam=llam)
    self.feats = feats
  def __getitem__(self, item):
    return self.feats[item] if item in self.feats else None
  def __repr__(self):
    if CAT in self.feats:
      return repr(self.feats[CAT])+':'+self.lex
    return self.lex
    
class HeadedToken(Token):
  def __getitem__(self, item):
    return self.head[item]

class FeatAltToken(HeadedToken):
  def __init__(self, head, feats={}):
    self.head = head
    self.feats = feats
    self.rlam = head.rlam
    self.llam = head.llam
  def __getitem__(self, item):
    return self.feats[item] if item in self.feats else self.head[item]

class Arg(FeatAltToken):
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
  def __repr__(self):
    return repr(self.head)+' ('+repr(self.arg)+')'

class ArgL(Arg):
  def __str__(self):
    return str(self.arg)+' '+str(self.head)
  def __repr__(self):
    return '('+repr(self.arg)+') '+repr(self.head)
    
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
  def __repr__(self):
    return repr(self.head)+' ['+repr(self.mod)+']'

class ModL(Mod):
  def __str__(self):
    return str(self.mod)+' '+str(self.head)
  def __repr__(self):
    return '['+repr(self.mod)+'] '+repr(self.head)

def get_verb_rlam(arg_pats):
  if len(arg_pats) == 0:
    return no_lam
  def verb_rlam(vp, other):
    if pat_matches(arg_pats[0], other):
      return ArgR(vp, other, feats={CAT: VP if len(arg_pats) == 1 else VB}, rlam=get_verb_rlam(arg_pats[1:]), llam=vp.llam)
  return verb_rlam

def get_verb_llam(subj_pat):
  def verb_llam(vp, other):
    if pat_matches(subj_pat, other):
      return ArgL(vp, other, rlam=vp.rlam, feats={HAS_SUBJ:True})
  return verb_llam

def get_verb_inter_rlam(subj_pat, arg_pats):
  def verb_rlam(vp, other):
    if pat_matches(subj_pat, other):
      return ArgR(vp, other, rlam=get_verb_rlam(arg_pats), feats={HAS_SUBJ:True})
  return verb_rlam

def get_verb_pass_rlam(subj):
  def verb_pass_rlam(v_pass, other):
    if pat_matches({CAT: V, FORM: PART, HAS_SUBJ: False}, other):
      res = other.rlam(other, FeatAltToken(subj, feats={CASE: ACC}))
      if res:
        return ArgR(v_pass, other, rlam=res.rlam)
  return verb_pass_rlam

def get_verb_pass_llam(subj_pat):
  def verb_pass_llam(v_pass, other):
    if pat_matches(subj_pat, other):
      return ArgL(v_pass, other, rlam=get_verb_pass_rlam(other), feats={HAS_SUBJ: True})
  return verb_pass_llam

def get_verb_pass_inter_rlam(subj_pat):
  def verb_pass_inter_rlam(v_pass, other):
    if pat_matches(subj_pat, other):
      return ArgR(v_pass, other, rlam=get_verb_pass_rlam(other), feats={HAS_SUBJ: True})
  return verb_pass_inter_rlam

def get_verb_aux_rlam(subj, arg_pat):
  def verb_aux_rlam(v_aux, other):
    if pat_matches({CAT: V, HAS_SUBJ: False}, other) and pat_matches(arg_pat, other):
      res = other.llam(other, subj)
      if res:
        return ArgR(v_aux, other, rlam=res.rlam)
  return verb_aux_rlam

def get_verb_aux_llam(subj_pat, arg_pat):
  def verb_aux_llam(v_aux, other):
    if pat_matches(subj_pat, other):
      return ArgL(v_aux, other, rlam=get_verb_aux_rlam(other, arg_pat), feats={HAS_SUBJ: True})
  return verb_aux_llam

def get_verb_aux_inter_rlam(subj_pat_arg_pat):
  def verb_aux_inter_rlam(v_aux, other):
    if pat_matches(subj_pat, other):
      return ArgR(v_aux, other, rlam=get_verb_aux_rlam(other, arg_pat), feats={HAS_SUBJ: True})

def nom_subj_pat(person, count):
  return {CAT: DP, CASE: NOM, PERSON: person, COUNT: count}
nom_subj_pat_any = nom_subj_pat(ANY, ANY)

class Verb(FeatToken):
  def __init__(self, lex, form, subj_pat, arg_pats):
    super().__init__(lex, {FORM: form, MOOD: DECL, CAT: V, HAS_SUBJ: False}, rlam=get_verb_rlam(arg_pats), llam=get_verb_llam(subj_pat))

class VerbInter(FeatToken):
  def __init__(self, lex, form, subj_pat, arg_pats):
    super().__init__(lex, {FORM: form, MOOD: INTER, CAT: V, HAS_SUBJ: False}, rlam=get_verb_inter_rlam(subj_pat, arg_pats))

class VerbPass(FeatToken):
  def __init__(self, lex, form, subj_pat):
    super().__init__(lex, {FORM: form, MOOD: DECL, CAT: V, HAS_SUBJ: False}, llam=get_verb_pass_llam(subj_pat))

class VerbPassInter(FeatToken):
  def __init__(self, lex, form, subj_pat):
    super().__init__(lex, {FORM: form, MOOD: INTER, CAT: V, HAS_SUBJ: False}, rlam=get_verb_pass_inter_rlam(subj_pat))

class VerbAux(FeatToken):
  def __init__(self, lex, form, subj_pat, arg_pat):
    super().__init__(lex, {FORM: form, MOOD: DECL, CAT: V, HAS_SUBJ: False}, llam=get_verb_aux_llam(subj_pat, arg_pat))

class VerbAuxInter(FeatToken):
  def __init__(self, lex, form, subj_pat, arg_pat):
    super().__init__(lex, {FORM: form, MOOD: INTER, CAT: V, HAS_SUBJ: False}, rlam=get_verb_aux_inter_rlam(subj_pat, arg_pat))

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

def poss_llam(poss, other):
  if matches(DP, other[CAT]):
    return ArgL(poss, other, rlam=det_rlam)

class Possessive(FeatToken):
  def __init__(self, lex):
    super().__init__(lex, {COUNT: ANY}, llam=poss_llam)

def adv_rlam(adv, other):
  if matches(VP, other[CAT]):
    return ModL(other, adv)
def adv_llam(adv, other):
  if matches(VP, other[CAT]):
    return ModR(other, adv)

class Adverb(FeatToken):
  def __init__(self, lex):
    super().__init__(lex, {CAT: Adv}, rlam=adv_rlam, llam=adv_llam)

def get_prep_mod_rlam(head_pat):
  def prep_llam(prep, other):
    if pat_matches(head_pat, other):
      return ModR(other, prep)
  def prep_rlam(prep, other):
    if matches(DP, other[CAT]):
      return ArgR(prep, other, feats={CAT: PP}, llam=prep_llam)
  return prep_rlam

class PrepositionMod(FeatToken):
  def __init__(self, lex, head_pat):
    super().__init__(lex, {LEX: lex}, rlam=get_prep_mod_rlam(head_pat))

def prep_rlam(prep, other):
  if matches(DP, other[CAT]):
    return ArgR(prep, other, feats={CAT: PP})

class Preposition(FeatToken):
  def __init__(self, lex):
    super().__init__(lex, {LEX: lex}, rlam=prep_rlam)

def get_comp_rlam(arg_pat):
  def comp_rlam(comp, other):
    if pat_matches(arg_pat, other) and matches(VP, other[CAT]):
      return ArgR(comp, other, feats={CAT: CP})
  return comp_rlam

class Complementizer(FeatToken):
  def __init__(self, lex, arg_pat):
    super().__init__(lex, {LEX: lex}, rlam=get_comp_rlam(arg_pat))

class ConjunctPhrase(Token):
  def __init__(self, lex, head_l, head_r):
    super().__init__(lex, rlam=mod_rlam, llam=mod_llam)
    self.head = head_l
    self.head_r = head_r
  def __str__(self):
    return str(self.head)+' '+self.lex+' '+str(self.head_r)
  def __repr__(self):
    return '('+repr(self.head)+') &:'+self.lex+' ('+repr(self.head_r)+')'
  def __getitem__(self, item):
    if matches(DP, self.head[CAT]) and item == COUNT:
      return PLUR
    else:
      return self.head[item]

def conj_rlam(conj, other_r):
  if other_r[CAT]:
    def conj_llam(conj, other_l):
      if matches(other_r[CAT], other_l[CAT]):
        return ConjunctPhrase(conj.lex, other_l, other_r)
    return Token(conj.lex, llam=conj_llam)

class Conjunction(Token):
  def __init__(self, lex):
    super().__init__(lex, rlam=conj_rlam)
