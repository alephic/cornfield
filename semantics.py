
# Fact properties
PRED = object()
ARG0 = object()
ARG1 = object()
INSTR = object()
GOAL = object()
MOTIV = object()
COND = object()
SUCC = object()
ANTE = object()
class UNK_PROP:
  def __init__(self, name):
    self.name = name
  def __eq__(self, other):
    return isinstance(other, UNK_PROP) and self.name == other.name
  def __hash__(self):
    return hash(UNK_PROP) ^ hash(self.name)

class Fact:
  def __init__(self, props):
    self.pred = pred
    self.props = props

class World:
  def __init__(self, facts):
    self.facts = facts

class Referent:
  def __init__(self, qualifiers):
    self.qualifiers = qualifiers