from util import multidict_add
from tags import *

known_tags = {}

def get_tags(lex):
  return known_tags[lex] if lex in known_tags else guess_tags(lex)

def guess_tags(lex):
  return [Noun(lex, PLUR if lex.endswith('s') else SING), PosAdjective(lex)]

def add_tok(tok):
  multidict_add(known_tags, tok.lex, tok)

add_tok(Determiner('the', [SING, PLUR]))
add_tok(Determiner('a', SING))
add_tok(Determiner('an', SING))
add_tok(FeatToken('i', {CAT: DP, CASE: NOM, COUNT: SING, PERSON: FIRST}))
add_tok(FeatToken('me', {CAT: DP, CASE: ACC, COUNT: SING, PERSON: FIRST}))
add_tok(FeatToken('myself', {CAT: DP, CASE: ACC, COUNT: SING, PERSON: FIRST}))
add_tok(Determiner('my', ANY))
add_tok(FeatToken('mine', {CAT: DP, CASE: ANY, COUNT: ANY, PERSON: THIRD}))
add_tok(FeatToken('we', {CAT: DP, CASE: NOM, COUNT: PLUR, PERSON: FIRST}))
add_tok(FeatToken('us', {CAT: DP, CASE: ACC, COUNT: PLUR, PERSON: FIRST}))
add_tok(FeatToken('ourselves', {CAT:DP, CASE: ACC, COUNT: PLUR, PERSON: FIRST}))
add_tok(Determiner('our', ANY))
add_tok(FeatToken('ours', {CAT: DP, CASE: ANY, COUNT: ANY, PERSON: THIRD}))
add_tok(FeatToken('you', {CAT: DP, CASE: ANY, COUNT: ANY, PERSON: SECOND}))
add_tok(FeatToken('yourself', {CAT: DP, CASE: ACC, COUNT: SING, PERSON: SECOND}))
add_tok(FeatToken('yourselves', {CAT: DP, CASE: ACC, COUNT: PLUR, PERSON: SECOND}))
add_tok(Determiner('your', ANY))
add_tok(FeatToken('yours', {CAT: DP, CASE: ANY, COUNT: ANY, PERSON: THIRD}))
add_tok(FeatToken('he', {CAT: DP, CASE: NOM, COUNT: SING, PERSON: THIRD}))
add_tok(FeatToken('him', {CAT: DP, CASE: ACC, COUNT: SING, PERSON: THIRD}))
add_tok(FeatToken('himself', {CAT: DP, CASE: ACC, COUNT: SING, PERSON: THIRD}))
add_tok(Determiner('his', ANY))
add_tok(FeatToken('his', {CAT: DP, CASE: ANY, COUNT: ANY, PERSON: THIRD}))
add_tok(FeatToken('it', {CAT: DP, CASE: ANY, COUNT: SING, PERSON: THIRD}))
add_tok(FeatToken('itself', {CAT: DP, CASE: ACC, COUNT: SING, PERSON: THIRD}))
add_tok(Determiner('its', ANY))
add_tok(FeatToken('its', {CAT: DP, CASE: ANY, COUNT: ANY, PERSON: THIRD}))
add_tok(FeatToken('they', {CAT: DP, CASE: NOM, COUNT: PLUR, PERSON: THIRD}))
add_tok(FeatToken('them', {CAT: DP, CASE: ACC, COUNT: PLUR, PERSON: THIRD}))
add_tok(FeatToken('themselves', {CAT: DP, CASE: ACC, COUNT: PLUR, PERSON: THIRD}))
add_tok(Determiner('their', ANY))
add_tok(FeatToken('theirs', {CAT: DP, CASE: ANY, COUNT: ANY, PERSON: THIRD}))
add_tok(FeatToken('that', {CAT: DP, CASE: ANY, COUNT: SING, PERSON: THIRD}))
add_tok(Determiner('that', SING))
add_tok(FeatToken('those', {CAT: DP, CASE: ANY, COUNT: PLUR, PERSON: THIRD}))
add_tok(Determiner('those', PLUR))
add_tok(FeatToken('this', {CAT: DP, CASE: ANY, COUNT: SING, PERSON: THIRD}))
add_tok(Determiner('this', SING))
add_tok(FeatToken('these', {CAT: DP, CASE: ANY, COUNT: PLUR, PERSON: THIRD}))
add_tok(Determiner('these', PLUR))
copula_arg_pat_base = [
  {CAT: VP, FORM: GERUND, HAS_SUBJ: False},
  {CAT: [Adj, PP]}
]
copula_arg_pat_sing = [{CAT: DP, CASE: ACC, COUNT: SING}]+copula_arg_pat_base
copula_arg_pat_plur = [{CAT: DP, CASE: ACC, COUNT: PLUR}]+copula_arg_pat_base
copula_arg_pat_any = [{CAT: DP, CASE: ACC, COUNT: ANY}]+copula_arg_pat_base
add_tok(Verb('am', PRES, FIRST, SING, copula_arg_pat_sing))
add_tok(Verb('are', PRES, ANY, PLUR, copula_arg_pat_any))
add_tok(Verb('are', PRES, SECOND, SING, copula_arg_pat_sing))
add_tok(Verb('is', PRES, THIRD, SING, copula_arg_pat_sing))
add_tok(Verb('was', PRET, [FIRST, THIRD], SING, copula_arg_pat_sing))
add_tok(Verb('were', PRET, SECOND, SING, copula_arg_pat_sing))
add_tok(Verb('were', PRET, SECOND, PLUR, copula_arg_pat_any))
add_tok(Verb('been', PART, ANY, ANY, copula_arg_pat_any))
add_tok(Verb('being', GERUND, ANY, ANY, copula_arg_pat_any))
add_tok(Verb('be', BASE, ANY, ANY, copula_arg_pat_any))
