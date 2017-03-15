
from collections import deque
from features import *

from trees import *

class FeatPred:
  def __init__(self, feat):
    self.feat = feat

class ClausePred:
  def __init__(self, root):
    self.root = root

class RefBox:
  def __init__(self, ref):
    self.ref = ref

class SpeakerRef:
  def __init__(self, speaker_id):
    self.speaker_id = speaker_id
  def __eq__(self, other):
    return isinstance(other, SpeakerRef) and self.speaker_id == other.speaker_id

class FixedRef(PredRef):
  def __init__(self, lex, preds):
    super().__init__(preds)
    self.lex = lex

class DetRef(PredRef):
  def __init__(self, deft, preds):
    super().__init__(preds)
    self.deft = deft

class MultiRef:
  def __init__(self, refs):
    self.refs = refs

MAX_MENTION_HISTORY = 100
MAX_AMBIG_MENTIONS = 10

class World:
  def __init__(self, referents):
    self.referents = referents
    self.mentions = deque(maxlen=MAX_MENTION_HISTORY)
    self.speaker = None
    self.interloc = None
  def process(self, stmt, speaker, interloc):
    self.speaker = speaker
    self.interloc = interloc
    for ref_node in collect_ref_nodes(stmt):
      ref = self.get_ref(ref_node)
      if isinstance(ref, PredRef):
        self.mentions.appendleft(ref)
  def get_pronoun_ref(self, node):
    if pronoun_person[node.stem] == FIRST:
      return self.speaker
    elif pronoun_person[node.stem] == SECOND:
      return self.interloc
    else:
      return self.get_mention(pronoun_plur[node.stem], pronoun_anim[node.stem], pronoun_gender[node.stem])
  def get_mention(self, *feats):
    matching = []
    for mention in self.mentions:
      matches = True
      for feat in feats:
        if isinstance(feat, AnyFeatVal):
          continue
        if not mention.has_feat(feat):
          matches = False
          break
      if matches:
        matching.append(mention)
        if len(matching) == MAX_AMBIG_MENTIONS:
          return MultiRef(matching)
    if len(matching) == 1:
      return matching[0]
    elif len(matching) > 1:
      return MultiRef(matching)
    else:
      return FixedRef('?', [FeatPred(f) for f in feats])
  def get_ref(self, node):
    if node.ref == None:
      self.gen_ref(node)
      self.referents.add(node.ref)
    return node.ref
  def gen_ref(self, node):
    if node.tag == 'PRP':
      node.ref = self.get_pronoun_ref(node)
    elif node.tag == 'PRP$':
      # TODO No such get_poss_pred implementation as of yet
      node.ref = PredRef(DEF, [self.get_poss_pred(self.get_pronoun_ref(node))])
    elif node.tag == 'DT':
      if node.stem in ('that', 'this'):
        node.ref = self.get_mention(INANIM, SING)
      elif node.stem in ('those', 'these'):
        node.ref = self.get_mention(INANIM, PLUR)
    elif (node.tag == 'NN' and 'det' not in node.children) or node.tag == 'NNP':
      node.ref = FixedRef(node.stem, [FeatPred(SING), FeatPred(feat_any(GENDER)), FeatPred(feat_any(ANIMACY))])
    elif node.tag in ('NN', 'NNS'):
      if 'det' in node.children:
        deft = INDEF if node.children['det'].stem in ('a','all','every','any','some') else DEF
      else:
        deft = INDEF
      plur = PLUR if node.tag == 'NNS' else SING
      node.ref = PredRef(deft, [FeatPred(feat_any(GENDER)), FeatPred(feat_any(ANIMACY)), FeatPred(plur)])
      for adj_reln in ['nmod', 'nmod:poss', 'acl', 'amod']:
        if adj_reln in node.children:
          for adjunct in node.children[adj_reln]:
            node.ref.preds.append(self.adjunct2pred(node, adjunct))
      if 'acl:relcl' in node.children:
        for relcl in node.children['acl:relcl']:
          self.handle_relcl(node, relcl)
  def adjunct2pred(self, subj_orig, adj_orig):
    # Reroot tree
    adj = adj_orig.deepcopy()
    adj.parent = None
    adj.reln = 'root'
    # Graft subject
    subj = subj_orig.deepcopy()
    subj.parent = adj
    subj.reln = 'nsubj'
    adj.children['nsubj'] = subj
    # Add copula
    cop = TreeNode('be', 'be', 'VBZ', 'cop', adj, {})
    adj.children['cop'] = cop
    return ClausePred(adj)
  def relcl2pred(self, subj_orig, relcl_orig):
    relcl = relcl_orig.deepcopy()
    relcl.parent = None
    relcl.reln = 'root'
    subj = subj_orig.deepcopy()
    if ('dobj' not in relcl.children) \
        or (relcl.children['dobj'].tag in ('WP', 'WDT')) \
        or ('nmod:poss' in relcl.children['dobj'].children \
          and relcl.children['dobj'].children['nmod:poss'].tag == 'WP$'):
      relcl.children['dobj'] = subj
    elif 'nsubj' in relcl.children \
        and (relcl.children['nsubj'].tag in ('WP', 'WDT') \
          or ('nmod:poss' in relcl.children['nsubj'].children \
            and relcl.children['nsubj'].children['nmod:poss'].tag == 'WP$')):
      relcl.children['nsubj'] = subj
    
      