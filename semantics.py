
from collections import deque

class TreeNode:
  def __init__(self, word, stem, tag, reln, parent, children):
    self.word = word
    self.stem = stem
    self.tag = tag
    self.reln = reln
    self.parent = parent
    self.children = children
  def __repr__(self):
    return '<'+self.word+':'+self.tag+'>'

def deps2tree(deps):
  nodes = list(map(lambda e: TreeNode(e[0], e[1], e[2], e[4], None, {}), deps))
  for ((w,s,t,d,r), n) in zip(deps, nodes):
    if d != -1:
      n.parent = nodes[d]
      if r in nodes[d].children:
        if isinstance(nodes[d].children[r], list):
          nodes[d].children[r].append(n)
        else:
          nodes[d].children[r] = [nodes[d].children[r], n]
      else:
        nodes[d].children[r] = n
  return nodes[0]

def tree_collect(tree, cond):
  if cond(tree):
    yield tree
  for child in tree.children.values():
    for node in tree_collect(child, cond):
      yield node

def collect_ref_nodes(tree):
  nominal_relns = ['nmod','nmod:poss','dobj','iobj','nsubj']
  nominal_tags = ['DT','PRP$','PRP','NN','NNP','NNS']
  return tree_collect(tree,
    lambda n: n.reln in nominal_relns or (n.reln == 'root' and n.tag in nominal_tags))

ANY = object()

def matches(pat, ex):
  if ex == ANY or pat == ANY:
    return True
  else return pat == ex

class InterlocRef:
  intrn = {}
  def __init__(self, pers, plur):
    self.pers = pers
    self.plur = plur
def get_interloc_ref(pers, plur=False):
  if (pers, plur) in InterlocRef.intrn:
    return InterlocRef.intrn[(pers, plur)]
  else:
    ref = InterlocRef(pers, plur)
    InterlocRef.intrn[(pers, plur)] = ref
    return ref

class FixedRef:
  intrn = {}
  def __init__(self, lex):
    self.lex = lex
def get_fixed_ref(lex):
  if lex in FixedRef.intrn:
    return FixedRef.intrn[lex]
  else:
    ref = FixedRef(lex)
    FixedRef.intrn[lex] = ref
    return ref

class World:
  def __init__(self, referents, relations):
    self.referents = referents
    self.relations = relations
    self.mentions = deque()
  def process(stmt, speaker_id):
    for ref_node in collect_ref_nodes(stmt):
      ref = self.get_ref_for(ref_node)
      self.mentions.appendleft(ref)
  def get_ref_for(node):
    if (node.tag == 'NN' and 'det' not in node.children) or node.tag == 'NNP':
      return FixedRef(node.stem)
    if node.tag == 'PRP':
      if node.stem == 'I' or node.stem == 'myself':
        return get_interloc_ref(1)
      if node.stem == 'we' or node.stem == 'ourselves':
        return get_interloc_ref(1, plur=True)
      if node.stem == 'you' or node.stem == 'yourself':
    # Indefinites become templates
    # Definites become templates restricted to existing referents
    # Pronouns are dereferenced to their last-mention buddy
    # nmods, acl:relcls and adjectives are exploded
    return None