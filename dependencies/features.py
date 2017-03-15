
class FeatVal:
  def __init__(self, key):
    self.key = key
  def __eq__(self, other):
    return isinstance(other, AnyFeatVal) or other == self

class AnyFeatVal(FeatVal):
  _intern = {}
  def __eq__(self, other):
    return isinstance(other, FeatVal)

def feat_any(key):
  if key in AnyFeatVal._intern:
    return AnyFeatVal._intern[key]
  else:
    new_any = AnyFeatVal(key)
    AnyFeatVal._intern[key] = new_any
    return new_any

def feat_dict(feats):
  return dict(map(lambda feat: (feat.key, feat), feats))

DEFT = object() # Definite/indefinite
DEF = FeatVal(DEFT)
INDEF = FeatVal(DEFT)

PLURALITY = object() # Plurality
SING = FeatVal(PLURALITY)
PLUR = FeatVal(PLURALITY)

GENDER = object() # Gender
MALE = FeatVal(GENDER)
FEMALE = FeatVal(GENDER)

ANIMACY = object() # Animacy
ANIM = FeatVal(ANIMACY)
INANIM = FeatVal(ANIMACY)

PERSON = object() # Speaker person
FIRST = FeatVal(PERSON)
SECOND = FeatVal(PERSON)
THIRD = FeatVal(PERSON)

pronoun_person = {
  'I': FIRST,
  'my': FIRST,
  'mine': FIRST,
  'myself': FIRST,
  'we': FIRST,
  'our': FIRST,
  'ours': FIRST,
  'ourselves': FIRST,
  'you': SECOND,
  'your': SECOND,
  'yours': SECOND,
  'yourself': SECOND,
  'yourselves': SECOND,
  'he': THIRD,
  'his': THIRD,
  'himself': THIRD,
  'she': THIRD,
  'her': THIRD,
  'hers': THIRD,
  'herself': THIRD,
  'they': THIRD,
  'their': THIRD,
  'themselves': THIRD,
  'it': THIRD,
  'its': THIRD,
  'itself': THIRD
}

pronoun_plur = {
  'I': SING,
  'my': SING,
  'mine': SING,
  'myself': SING,
  'we': PLUR,
  'our': PLUR,
  'ours': PLUR,
  'ourselves': PLUR,
  'you': feat_any(PLURALITY),
  'your': feat_any(PLURALITY),
  'yours': feat_any(PLURALITY),
  'yourself': SING,
  'yourselves': PLUR,
  'he': SING,
  'his': SING,
  'himself': SING,
  'she': SING,
  'her': SING,
  'hers': SING,
  'herself': SING,
  'they': feat_any(PLURALITY),
  'their': feat_any(PLURALITY),
  'themselves': feat_any(PLURALITY),
  'it': SING,
  'its': SING,
  'itself': SING
}

pronoun_gender = {
  'he': MALE,
  'his': MALE,
  'himself': MALE,
  'she': FEMALE,
  'her': FEMALE,
  'hers': FEMALE,
  'herself': FEMALE,
  'they': feat_any(GENDER),
  'their': feat_any(GENDER),
  'themselves': feat_any(GENDER),
  'it': feat_any(GENDER),
  'its': feat_any(GENDER),
  'itself': feat_any(GENDER)
}

pronoun_anim = {
  'he': ANIM,
  'his': ANIM,
  'himself': ANIM,
  'she': ANIM,
  'her': ANIM,
  'hers': ANIM,
  'herself': ANIM,
  'they': feat_any(ANIM),
  'their': feat_any(ANIM),
  'themselves': feat_any(ANIM),
  'it': INANIM,
  'its': INANIM,
  'itself': INANIM
}