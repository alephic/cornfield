from util import multidict_add
from tags import *

known_tags = {}

vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxz'

def get_tpsingpres_form(base_form):
  if base_form[-1] == 'y' and base_form[-2] not in vowels:
    return base_form[:-1]+'ies'
  for sib_suf in ['s','sh','z','tch']:
    if base_form.endswith(sib_suf):
      return base_form+'es'
  return base_form+'s'

def get_pret_form(base_form):
  if base_form[-1] == 'y' and base_form[-2] not in vowels:
    return base_form[:-1]+'ies'
  return base_form+'d' if base_form[-1] == 'e' else base_form+'ed'

def get_gerund_form(base_form):
  if base_form.endswith('ie'):
    return base_form[:-2]+'ying'
  return base_form[:-1]+'ing' if base_form[-1] == 'e' else base_form+'ing'

def add_verb(head, form, *arg_preds):
  multidict_add(known_tags, head, V(head, form, [], arg_preds))
def add_verb_auto(forms, *arg_preds):
  add_verb(forms[BASE], BASE, *arg_preds)
  if TPSINGPRES in forms:
    add_verb(forms[TPSINGPRES], TPSINGPRES, *arg_preds)
  else:
    add_verb(get_tpsingpres_form(forms[BASE]), TPSINGPRES, *arg_preds)
  pret_form = forms[PRET] if PRET in forms else get_pret_form(forms[BASE])
  add_verb(pret_form, PRET, *arg_preds)
  if PART in forms:
    add_verb(forms[PART], PART, *arg_preds)
  else:
    add_verb(pret_form, PART, *arg_preds)
  add_verb(get_gerund_form(forms[BASE]), GERUND, *arg_preds)
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
def add_det(head, deft, count, restrict=None, person=3):
  multidict_add(known_tags, head, D(head, deft, count, restrict, person))
def add_dp(head, deft, count, qualifiers, restrict=None, person=3):
  multidict_add(known_tags, head, DP(head, deft, count, qualifiers, restrict, person))

multidict_add(known_tags, ',', list_comma_tag)
multidict_add(known_tags, '\'s', poss_suff_tag)
multidict_add(known_tags, 'and', Conj('and'))
add_det('the', DEF, UNSPEC)
add_det('a', INDEF, SING)
add_det('an', INDEF, SING)
add_det('some', INDEF, PLUR)
add_det('his', DEF, UNSPEC)
add_dp('his', DEF, UNSPEC, Pronoun(None))
add_dp('he', DEF, SING, Pronoun(MASC), restrict=SUBJ)
add_dp('him', DEF, SING, Pronoun(MASC), restrict=OBJ)
add_dp('himself', DEF, SING, Pronoun(MASC, reflexive=True), restrict=OBJ)
add_det('her', DEF, UNSPEC)
add_dp('hers', DEF, UNSPEC, Pronoun(None))
add_dp('she', DEF, SING, Pronoun(FEM), restrict=SUBJ)
add_dp('her', DEF, SING, Pronoun(FEM), restrict=OBJ)
add_dp('herself', DEF, SING, Pronoun(FEM, reflexive=True), restrict=OBJ)
add_det('its', DEF, UNSPEC)
add_dp('its', DEF, UNSPEC, Pronoun(None))
add_dp('it', DEF, SING, Pronoun(NEUT))
add_dp('itself', DEF, SING, Pronoun(NEUT, reflexive=True), restrict=OBJ)
add_det('their', DEF, UNSPEC)
add_dp('theirs', DEF, UNSPEC, Pronoun(None))
add_dp('they', DEF, PLUR, Pronoun(None), restrict=SUBJ)
add_dp('them', DEF, PLUR, Pronoun(None), restrict=OBJ)
add_dp('themselves', DEF, PLUR, Pronoun(None, reflexive=True), restrict=OBJ)
add_det('my', DEF, UNSPEC)
add_dp('mine', DEF, UNSPEC, Pronoun(None))
add_dp('i', DEF, SING, Pronoun(None), restrict=SUBJ, person=1)
add_dp('me', DEF, SING, Pronoun(None), restrict=OBJ, person=1)
add_dp('myself', DEF, SING, Pronoun(None, reflexive=True), restrict=OBJ)
add_det('our', DEF, UNSPEC)
add_dp('ours', DEF, UNSPEC, Pronoun(None))
add_dp('we', DEF, PLUR, Pronoun(None), restrict=SUBJ, person=1)
add_dp('us', DEF, PLUR, Pronoun(None), restrict=OBJ, person=1)
add_dp('ourselves', DEF, PLUR, Pronoun(None, reflexive=True), restrict=OBJ, person=1)
add_det('your', DEF, UNSPEC)
add_dp('yours', DEF, UNSPEC, Pronoun(None))
add_dp('you', DEF, UNSPEC, Pronoun(None), person=2)
add_dp('yourself', DEF, SING, Pronoun(None, reflexive=True), restrict=OBJ, person=2)
add_dp('yourselves', DEF, PLUR, Pronoun(None, reflexive=True), restrict=OBJ, person=2)
add_dp('that', DEF, SING, Pronoun(None))
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
copula_arg_pred = pred_or(tag_p(DP), tag_p(PP), tag_p(Adj))
add_verb('be', BASE, copula_arg_pred)
add_verb('am', FPSINGPRES, copula_arg_pred)
add_verb('are', PLURPRES, copula_arg_pred)
add_verb('was', SINGPRET, copula_arg_pred)
add_verb('were', PLURPRET, copula_arg_pred)
add_verb('being', GERUND, copula_arg_pred)
add_verb('been', PART, copula_arg_pred)
add_verb_auto({BASE:'do', PRET:'did', PART:'done'}, tag_p(DP))
add_verb_auto({BASE:'have', TPSINGPRES:'has', PRET:'had'},
  pred_or(tag_p(DP), vp_form_p(PART)))
add_verb_auto({BASE:'go', PRET:'went', PART:'gone'},
  pred_or(tag_head_p(PP, 'to'), tag_head_p(PP, 'back')))

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
