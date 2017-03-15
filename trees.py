
class TreeNode:
  def __init__(self, word, stem, tag, reln, parent, children, ref_box=None):
    self.word = word
    self.stem = stem
    self.tag = tag
    self.reln = reln
    self.parent = parent
    self.children = children
    self.ref_box = None
  def __repr__(self):
    return '<'+self.word+':'+self.tag+'>'
  def collect(self, cond):
    if cond(self):
      yield self
    for child in self.children.values():
      for node in child.collect(cond):
        yield node
  def add_child(self, child):
    if child.reln in self.children:
      if isinstance(self.children[child.reln], list):
        self.children[child.reln].append(child)
      else:
        self.children[child.reln] = [self.children[child.reln], child]
    else:
      self.children[child.reln] = child
  def __iter__(self):
    yield self
  def __getitem__(self, item):
    if item == 0:
      return self
    else:
      raise ValueError()
  def __len__(self):
    return 1
  def deepcopy(self):
    copy = TreeNode(self.word, self.stem, self.tag, self.reln, self.parent, dict(), ref_box=self.ref_box)
    for child in self.children.values():
      copy.add_child(child.deepcopy())

def deps2tree(deps):
  nodes = list(map(lambda e: TreeNode(e[0], e[1], e[2], e[4], None, {}), deps))
  for ((w,s,t,d,r), n) in zip(deps, nodes):
    if d != -1:
      n.parent = nodes[d].add_child(n)
  return nodes[0]

def collect_ref_nodes(tree):
  nominal_relns = ['nmod','nmod:poss','dobj','iobj','nsubj','nsubjpass']
  nominal_tags = ['DT','PRP$','PRP','NN','NNP','NNS']
  return tree.collect(lambda n: n.reln in nominal_relns or (n.reln == 'root' and n.tag in nominal_tags))