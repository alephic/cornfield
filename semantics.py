from tags import *

# Fact properties
PRED = object()
ARG0 = object()
ARG1 = object()
INSTR = object()
GOAL = object()
MOTIV = object()
COND = object()
# Special properties
PASS = object()
class NAMED_PROP:
  def __init__(self, name):
    self.name = name
  def __eq__(self, other):
    return isinstance(other, NAMED_PROP) and self.name == other.name
  def __hash__(self):
    return hash(NAMED_PROP) ^ hash(self.name)

class Fact:
  def __init__(self, props):
    self.props = props

class World:
  def __init__(self, facts):
    self.facts = facts

class Qualifier:
  pass
class PronounQual(Qualifier):
  pass
class PropertyQual(Qualifier):
  pass
class Referent:
  def __init__(self, qualifiers):
    self.qualifiers = qualifiers