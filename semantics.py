from util import DefaultDict

class TreeNode:
  def __init__(self, word, tag, reln, parent, children):
    self.word = word
    self.tag = tag
    self.reln = reln
    self.parent = parent
    self.children = children

def deps2tree(deps):
  nodes = list(map(lambda e: TreeNode(e[0], e[1], e[3], None, []), deps))
  for ((w,t,d,r), n) in zip(deps, nodes):
    if d != -1:
      n.parent = nodes[d]
      nodes[d].children.append(n)
  return nodes[0]

# Semantic features
# Of predicates:
DEFAULT = object()

# Time
TIME = object()
# Values:
PRES = object() # Present
PAST = object() # Past
FUT = object() # Future

# Aspect
ASPECT = object()
# Values:
CONT = object() # Continuing

# Mode
MODE = object()
# Values:
NECESS = object()
DEMAND = object()
HYPOTH = object()
CAPABL = object()
HABIT = object()

