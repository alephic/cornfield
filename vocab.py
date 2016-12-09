from util import multidict_add
from tags import *

known_tags = {}

vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxz'

def get_tpsingpres_form(base_form):
  if base_form[-1] == 'y' and base_form[-2] in consonants:
    return base_form[:-1]+'ies'
  for sib_suf in ['s','sh','z','tch']:
    if base_form.endswith(sib_suf):
      return base_form+'es'
  return base_form+'s'

def add_verb(head, form, *arg_preds):
  multidict_add(known_tags, head, V(head, form, [], arg_preds))
def add_verb_auto(base_form, *arg_preds):
  add_verb(base_form, BASE, *arg_preds)
  add_verb(get_tpsingpres_form(base_form), TPSINGPRES, *arg_preds)
  add_verb(get_pret_form(base_form), PRET, *arg_preds)
  add_verb(get_pret_form(base_form), PART, *arg_preds)
  add_verb(get_gerund_form(base_form), GERUND, *arg_preds)
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
def add_dp(head, deft, count, qualifiers, restrict=None, person=3):
  multidict_add(known_tags, head, DP(head, deft, count, qualifiers, restrict=restrict, person=person))

add_det('the', DEF, SING)
add_det('the', DEF, PLUR)
add_det('a', INDEF, SING)
add_det('an', INDEF, SING)
add_det('some', INDEF, PLUR)
add_dp('he', DEF, SING, [Gender(MASC), Pronoun()], restrict=SUBJ)
add_dp('him', DEF, SING, [Gender(MASC), Pronoun()], restrict=OBJ)
add_dp('himself', DEF, SING, [Gender(MASC), Pronoun(reflexive=True)], restrict=OBJ)
add_dp('she', DEF, SING, [Gender(FEM), Pronoun()], restrict=SUBJ)
add_dp('her', DEF, SING, [Gender(FEM), Pronoun()], restrict=OBJ)
add_dp('herself', DEF, SING, [Gender(FEM), Pronoun(reflexive=True)], restrict=OBJ)
add_dp('it', DEF, SING, [Gender(NEUT), Pronoun()])
add_dp('itself', DEF, SING, [Pronoun(reflexive=True)], restrict=OBJ)
add_dp('they', DEF, PLUR, [Pronoun()], restrict=SUBJ)
add_dp('them', DEF, PLUR, [Pronoun()], restrict=OBJ)
add_dp('themselves', DEF, PLUR, [Pronoun(reflexive=True)], restrict=OBJ)
add_dp('i', DEF, SING, [Pronoun()], restrict=SUBJ, person=1)
add_dp('me', DEF, SING, [Pronoun()], restrict=OBJ, person=1)
add_dp('myself', DEF, SING, [Pronoun(reflexive=True)], restrict=OBJ)
add_dp('we', DEF, PLUR, [Pronoun()], restrict=SUBJ, person=1)
add_dp('us', DEF, PLUR, [Pronoun()], restrict=OBJ, person=1)
add_dp('ourselves', DEF, PLUR, [Pronoun(reflexive=True)], restrict=OBJ, person=1)
add_dp('you', DEF, SING, [Pronoun()], person=2)
add_dp('you', DEF, PLUR, [Pronoun()], person=2)
add_dp('yourself', DEF, SING, [Pronoun(reflexive=True)], restrict=OBJ, person=2)
add_dp('yourselves', DEF, PLUR, [Pronoun(reflexive=True)], restrict=OBJ, person=2)
add_prep('at')
add_prep('to')
add_prep('with')
add_prep('in')
add_prep('on')
add_prep('above')
add_prep('below')
add_pp('back')
add_pp('around')
add_prep_mod('of')
add_prep_mod('with')
# Copula
copula_arg_pred = pred_or(tag(DP), tag(PP), tag(Adj))
add_verb('be', BASE, copula_arg_pred)
add_verb('am', FPSINGPRES, copula_arg_pred)
add_verb('are', PLURPRES, copula_arg_pred)
add_verb('was', SINGPRET, copula_arg_pred)
add_verb('were', PLURPRET, copula_arg_pred)
add_verb('being', GERUND, copula_arg_pred)
add_verb('been', PART, copula_arg_pred)

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
