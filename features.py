
class FeatVal:
  def __init__(self, feature):
    self.feature = feature
  def __eq__(self, other):
    return isinstance(other, AnyFeatVal) or other == self

class AnyFeatVal(FeatVal):
  _intern = {}
  def __eq__(self, other):
    return isinstance(other, FeatVal)

def feat_any(feat):
  if feat in AnyFeatVal._intern:
    return AnyFeatVal._intern[feat]
  else:
    new_any = AnyFeatVal(feat)
    AnyFeatVal._intern[feat] = new_any
    return new_any

def feat_dict(feats):
  return dict(map(lambda feat: (feat.feature, feat), feats))

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