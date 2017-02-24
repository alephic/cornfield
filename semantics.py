
from collections import deque
from features import *

from trees import *

class FeatPred:
  def __init__(self, feat):
    self.feat = feat

class ClausePred:
  def __init__(self, root):
    self.root = root

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
  def __init__(self, referents, relations):
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
      ref = self.gen_ref(node)
      self.referents.add(ref)
      node.ref = ref
    return node.ref
  def gen_ref(self, node):
    if node.tag == 'PRP':
      return self.get_pronoun_ref(node)
    elif node.tag == 'PRP$':
      return PredRef(DEF, [PossPred(self.get_pronoun_ref(node))])
    elif node.tag == 'DT':
      if node.stem in ('that', 'this'):
        return self.get_mention(INANIM, SING)
      elif node.stem in ('those', 'these'):
        return self.get_mention(INANIM, PLUR)
    elif (node.tag == 'NN' and 'det' not in node.children) or node.tag == 'NNP':
      return FixedRef(node.stem, [FeatPred(SING), FeatPred(feat_any(GENDER)), FeatPred(feat_any(ANIMACY))])
    elif node.tag in ('NN', 'NNS'):
      if 'det' in node.children:
        deft = INDEF if node.children['det'].stem in ('a','all','every','any','some') else DEF
      else:
        deft = INDEF
      plur = PLUR if node.tag == 'NNS' else SING
      ref = PredRef(deft, [FeatPred(feat_any(GENDER)), FeatPred(feat_any(ANIMACY)), FeatPred(plur)])
      # Add copular ClausePreds for n/adj adjuncts
      # Add ClausePreds for relcls
      return ref