from tags import *

nouns = [
  'object',
  'thing',
  'place'
]
nouns_infl = {
  'person': 'people',
  'man': 'men',
  'woman': 'women'
}
def get_plural(noun):
  if noun in nouns_infl:
    return nouns_infl[noun]
  else:
    return noun+'es' if noun.endswith('s') else noun+'s'

adjs = [
  'small',
  'large',
  'little',
  'big',
  'red',
  'green',
  'blue',
  'yellow',
  'orange',
  'cyan',
  'pink',
  'purple',
  'teal',
  'brown',
  'tan',
  'maroon',
  'thin',
  'thick',
  'tall',
  'short',
  'round',
  'sharp',
  'gold',
  'golden',
  'good',
  'bad'
]

known_tags = {}

def add_verb(head, *arg_preds):
  multidict_add(known_tags, head, V(head, [], arg_preds))
def add_noun(head):
  multidict_add(known_tags, head, NP(SING, [N(head)]))
def add_plur_noun(head):
  multidict_add(known_tags, head, NP(PLUR, [N(head)]))
def add_adj(head):
  multidict_add(known_tags, head, Adj(head))
def add_prep(head):
  multidict_add(known_tags, head, P(head))
def add_pp(head):
  multidict_add(known_tags, head, PP(head, None))
def add_prep_mod(head):
  multidict_add(known_tags, head, PM(head))
def add_adv(head):
  multidict_add(known_tags, head, Adv(head))
def add_det(head, deft, count):
  multidict_add(known_tags, head, D(head, deft, count))
def add_dp(head, deft, count, qualifiers):
  multidict_add(known_tags, head, DP(head, deft, count, qualifiers))

add_det('the', DEF, SING)
add_det('the', DEF, PLUR)
add_det('a', INDEF, SING)
add_det('an', INDEF, SING)
add_det('some', INDEF, PLUR)
add_dp('him', DEF, SING, [Gender(MASC)])
add_dp('her', DEF, SING, [Gender(FEM)])
add_dp('it', DEF, SING, [Gender(NEUT)])
add_dp('them', DEF, PLUR, [])
add_prep('at')
add_prep('to')
add_prep('with')
add_prep('in')
add_prep('on')
add_prep('above')
add_prep('below')
add_pp('back')
add_prep_mod('of')
add_prep_mod('with')
add_adv('around')
add_adv('back')
add_adv('carefully')
add_adv('closely')
add_verb('look', tag_head(PP, 'at'))
add_verb('examine', tag(DP))
add_verb('go', tag_head(PP, 'to'))
add_verb('go', tag_head(PP, 'back'))
add_verb('put', tag(DP), tag_head(PP, 'on'))
add_verb('give', tag(DP), tag(DP))
add_verb('give', tag(DP), tag_head(PP, 'to'))
add_verb('open', tag(DP))
add_verb('open', tag(DP), tag_head(PP, 'with'))
add_verb('close', tag(DP))
add_verb('throw', tag(DP), tag_head(PP, 'at'))
for noun in nouns:
  add_noun(noun)
  add_plur_noun(vocab.get_plural(noun))
for adj in adjs:
  add_adj(adj)

def guess_tags(word):
  if word.endswith('ly'):
    return [Adv(word)]
  res = [
    Adj(word),
    NP(PLUR if word.endswith('s') else SING, [N(word)])
  ]
  return res

def get_tags(word):
  return known_tags[word] if word in known_tags else guess_tags(word)
