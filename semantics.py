
class TreeNode:
  def __init__(self, word, stem, tag, reln, parent, children):
    self.word = word
    self.stem = stem
    self.tag = tag
    self.reln = reln
    self.parent = parent
    self.children = children

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

def directly_implies(tree1, tree2):
  pass