
# Person
PERSON = object()
FIRST = object()
SECOND = object()
THIRD = object()

# Case
CASE = object()
NOM = object()
ACC = object()

# Gender
GENDER = object()
MASC = object()
FEM = object()
NEUT = object()

# Count
COUNT = object()
SING = object()
PLUR = object()

# Definiteness
DEFT = object()
DEF = object()
INDEF = object()

# Verb tense/aspect
FORM = object()
PRET = object()
PRES = object()
PART = object()
GERUND = object()

class Tag(dict):
  rlam = None
  llam = None
  head = None
  def satisfies(self, cat):
    return cat == self.__class__
  def __getitem__(self, item):
    if item in self:
      return super().__getitem__(self, item)
    elif self.head:
      return self.head[item]
    else:
      return None

class N(Tag):
  def __init__(self, text, count):
    self.text = text
    self[COUNT] = count
  def __str__(self):
    return self.text
  def satisfies(self, cat):
    return cat in (N, NP) or (cat == DP and self[COUNT] == PLUR)
  def rlam(self, tok):
    if tok.satisfies(N):
      return LMod(tok, self)

class DP(Tag):
  def __init__(self, head, arg):
    self.head = head
    self.arg = arg

class RMod(Tag):
  def __init__(self, head, mod):
    self.head = head
    self.mod = mod
  def __str__(self):
    return str(self.head)+' '+str(self.mod)
  def satisfies(self, cat):
    return self.head.satisfies(cat)

class LMod(Tag):
  def __init__(self, head, mod):
    self.head = head
    self.mod = mod
  def __str__(self):
    return str(self.mod)+' '+str(self.head)
  def satisfies(self, cat):
    return self.head.satisfies(cat)
