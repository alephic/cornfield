
class TreeNode:
  def __init__(self, word, tag, reln, children):
    self.word = word
    self.tag = tag
    self.reln = reln
    self.children = children

def deps2tree(deps):
  nodes = list(map(lambda e: TreeNode(e[0],e[1],e[3],[]), deps))
  for ((w,t,d,r), n) in zip(deps, nodes):
    if d != -1:
      nodes[d].children.append(n)
  return nodes[0]

class SemanticNode:
  def __init__(self):
    pass