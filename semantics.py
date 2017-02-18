
from collections import deque
from features import *

class TreeNode:
  def __init__(self, word, stem, tag, reln, parent, children):
    self.word = word
    self.stem = stem
    self.tag = tag
    self.reln = reln
    self.parent = parent
    self.children = children
    self.ref = None
  def __repr__(self):
    return '<'+self.word+':'+self.tag+'>'
  def collect(self, cond):
    if cond(self):
      yield self
    for child in self.children.values():
      for node in child.collect(cond):
        yield node

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

def collect_ref_nodes(tree):
  nominal_relns = ['nmod','nmod:poss','dobj','iobj','nsubj','nsubjpass']
  nominal_tags = ['DT','PRP$','PRP','NN','NNP','NNS']
  return tree.collect(lambda n: n.reln in nominal_relns or (n.reln == 'root' and n.tag in nominal_tags))

class SpeakerRef:
  _intern = {}
  def __init__(self, pers, plur):
    self.pers = pers
    self.plur = plur
  def __eq__(self, other):
    return isinstance(other, SpeakerRef) and self.pers == other.pers and self.plur == other.plur
  def __hash__(self, other):
    return hash(SpeakerRef) ^ hash(self.pers) ^ hash(self.plur)
def get_speaker_ref(pers, plur):
  if (pers, plur) in SpeakerRef._intern:
    return SpeakerRef._intern[(pers, plur)]
  else:
    ref = SpeakerRef(pers, plur)
    SpeakerRef._intern[(pers, plur)] = ref
    return ref

class FixedRef:
  _intern = {}
  def __init__(self, lex):
    self.lex = lex
def get_fixed_ref(lex):
  if lex in FixedRef._intern:
    return FixedRef._intern[lex]
  else:
    ref = FixedRef(lex)
    FixedRef._intern[lex] = ref
    return ref

class QualRef:
  def __init__(self, deft, quals):
    self.deft = deft
    self.quals = quals
  def has_feat(self, feat):
    for qual in self.quals:
      if isinstance(qual, FeatQual):
        if qual.feat == feat:
          return True
  def specify_feat_quals(self, feats):
    d = feat_dict(feats)
    for qual in self.quals:
      if isinstance(qual, FeatQual) and isinstance(qual.feat, AnyFeatVal) and qual.feat.feature in d:
        qual.feat = d[qual.feat.feature]

class FeatQual:
  def __init__(self, feat):
    self.feat = feat

MAX_MENTION_HISTORY = 100

class World:
  def __init__(self, referents, relations):
    self.referents = referents
    self.relations = relations
    self.mentions = deque(maxlen=MAX_MENTION_HISTORY)
  def process(stmt, speaker_id):
    for ref_node in collect_ref_nodes(stmt):
      ref = self.get_ref(ref_node)
      if isinstance(ref, QualRef):
        self.mentions.appendleft(ref)
  def get_mention(self, *feats):
    for mention in self.mentions:
      matches = True
      for feat in feats:
        if not mention.has_feat(feat):
          matches = False
          break
      if matches:
        mention.specify_feat_quals(feats)
        return mention
  def get_ref(node):
    if node.ref == None:
      ref = self.gen_ref(node)
      node.ref = ref
    return node.ref
  def gen_ref(node):
    if node.tag == 'PRP':
      if pronoun_person[node.stem] in (FIRST, SECOND):
        return SpeakerRef(pronoun_person[node.stem], pronoun_plur[node.stem])
      elif node.stem in ('it', 'itself'):
        return self.get_mention(INANIM, SING)
      elif node.stem in ('they', 'themselves'):
        return self.get_mention(PLUR)
      elif node.stem in ('he', 'himself'):
        return self.get_mention(ANIM, MALE)
      elif node.stem in ('she', 'herself'):
        return self.get_mention(ANIM, FEMALE)
    elif node.tag == 'DT':
      if node.stem in ('that', 'this'):
        return self.get_mention(INANIM, SING)
      elif node.stem in ('those', 'these'):
        return self.get_mention(INANIM, PLUR)
    elif (node.tag == 'NN' and 'det' not in node.children) or node.tag == 'NNP':
      return FixedRef(node.stem, [FeatQual(feat_any(GENDER)), FeatQual(feat_any(ANIMACY))])
    elif node.tag in ('NN', 'NNS'):
      if 'det' in node.children:
        deft = INDEF if node.children['det'].stem in ('a','all','every','any','some') else DEF
      else:
        deft = INDEF
      plur = PLUR if node.tag == 'NNS' else SING
      ref = QualRef(deft, [FeatQual(feat_any(GENDER)), FeatQual(feat_any(ANIMACY)), FeatQual(plur)])
      if 'compound' in node.children:
        for c in node.children['compound']:
          ref.quals.append(CompoundQual(c))
      if 'amod' in node.children:
        for c in node.children['amod']:
          ref.quals.append(AdjectiveQual(c))
      if 'nmod' in node.children:
        for c in node.children['nmod']:
          ref.quals.append(self.get_nmod_qual(c))
      if 'nmod:poss' in node.children:
        ref.quals.append(self.get_poss_qual(node.children['nmod:poss']))
      if 'acl:relcl' in node.children:
        ref.quals.append(self.get_relcl_qual(node.children['acl:relcl']))
      if 'acl' in node.children:
        ref.quals.append(self.get_acl_qual(node.children['acl']))
      return ref
    elif node.tag == 'PRP$':
      return QualRef(DEF, [PossQual()])