
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

def gather_relations(tree):
  n_rels = ['nsubj', 'dobj', 'nmod', 'nmod:poss']
  n_tags = ['NN','NNP','NNS','PRP','PRP$']
  n_nodes = tree_collect(tree, lambda node: node.reln in n_rels or node.tag in n_tags)
  return list(n_nodes)