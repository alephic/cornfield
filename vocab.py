from util import multidict_add
from tags import *

known_tags = {}
postfixes = ['\'s', '\'ve', '\'d', '\'m', '\'re', '\'ll', ',', '.', '?', '!']

def get_tags(lex):
  return known_tags[lex] if lex in known_tags else guess_tags(lex)

def guess_tags(lex):
  if lex.endswith('ly'):
    return [Adverb(lex)]
  return [Noun(lex, PLUR if lex.endswith('s') else SING), PosAdjective(lex)]

def add_tok(tok):
  multidict_add(known_tags, tok.lex, tok)
  
add_tok(Conjunction('and'))
add_tok(Conjunction('or'))

add_tok(Possessive('\'s'))
add_tok(PrepositionMod('of', {CAT: NP}))
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
add_tok(FeatToken('she', {CAT: DP, CASE: NOM, COUNT: SING, PERSON: THIRD}))
add_tok(FeatToken('her', {CAT: DP, CASE: ACC, COUNT: SING, PERSON: THIRD}))
add_tok(FeatToken('herself', {CAT: DP, CASE: ACC, COUNT: SING, PERSON: THIRD}))
add_tok(Determiner('her', ANY))
add_tok(FeatToken('hers', {CAT: DP, CASE: ANY, COUNT: ANY, PERSON: THIRD}))
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

copula_arg_pats_base = [
  {CAT: VP, FORM: GERUND, HAS_SUBJ: False},
  {CAT: [Adj, PP]}
]
copula_arg_pats_sing = [[{CAT: DP, CASE: ACC, COUNT: SING}]+copula_arg_pats_base]
copula_arg_pats_plur = [[{CAT: DP, CASE: ACC, COUNT: PLUR}]+copula_arg_pats_base]
copula_arg_pats_any = [[{CAT: DP, CASE: ACC, COUNT: ANY}]+copula_arg_pats_base]
# Copular verb
add_tok(Verb('am', PRES, nom_subj_pat(FIRST, SING), copula_arg_pats_sing))
add_tok(Verb('\'m', PRES, nom_subj_pat(FIRST, SING), copula_arg_pats_sing))
add_tok(Verb('are', PRES, nom_subj_pat(ANY, PLUR), copula_arg_pats_any))
add_tok(Verb('\'re', PRES, nom_subj_pat(ANY, PLUR), copula_arg_pats_any))
add_tok(Verb('are', PRES, nom_subj_pat(SECOND, SING), copula_arg_pats_sing))
add_tok(Verb('is', PRES, nom_subj_pat(THIRD, SING), copula_arg_pats_sing))
add_tok(Verb('\'s', PRES, nom_subj_pat(THIRD, SING), copula_arg_pats_sing))
add_tok(Verb('was', PRET, nom_subj_pat([FIRST, THIRD], SING), copula_arg_pats_sing))
add_tok(Verb('were', PRET, nom_subj_pat(SECOND, SING), copula_arg_pats_sing))
add_tok(Verb('were', PRET, nom_subj_pat(ANY, PLUR), copula_arg_pats_any))
add_tok(VerbInter('am', PRES, nom_subj_pat(FIRST, SING), copula_arg_pats_sing))
add_tok(VerbInter('\'m', PRES, nom_subj_pat(FIRST, SING), copula_arg_pats_sing))
add_tok(VerbInter('are', PRES, nom_subj_pat(ANY, PLUR), copula_arg_pats_any))
add_tok(VerbInter('\'re', PRES, nom_subj_pat(ANY, PLUR), copula_arg_pats_any))
add_tok(VerbInter('are', PRES, nom_subj_pat(SECOND, SING), copula_arg_pats_sing))
add_tok(VerbInter('is', PRES, nom_subj_pat(THIRD, SING), copula_arg_pats_sing))
add_tok(VerbInter('was', PRET, nom_subj_pat([FIRST, THIRD], SING), copula_arg_pats_sing))
add_tok(VerbInter('were', PRET, nom_subj_pat(SECOND, SING), copula_arg_pats_sing))
add_tok(VerbInter('were', PRET, nom_subj_pat(SECOND, PLUR), copula_arg_pats_any))
add_tok(Verb('been', PART, nom_subj_pat_any, copula_arg_pats_any))
add_tok(Verb('being', GERUND, nom_subj_pat_any, copula_arg_pats_any))
add_tok(Verb('be', BARE, nom_subj_pat_any, copula_arg_pats_any))

# Passive verb
add_tok(VerbPass('am', PRES, nom_subj_pat(FIRST, SING)))
add_tok(VerbPass('\'m', PRES, nom_subj_pat(FIRST, SING)))
add_tok(VerbPass('are', PRES, nom_subj_pat(ANY, PLUR)))
add_tok(VerbPass('\'re', PRES, nom_subj_pat(ANY, PLUR)))
add_tok(VerbPass('are', PRES, nom_subj_pat(SECOND, SING)))
add_tok(VerbPass('is', PRES, nom_subj_pat(THIRD, SING)))
add_tok(VerbPass('\'s', PRES, nom_subj_pat(THIRD, SING)))
add_tok(VerbPass('was', PRET, nom_subj_pat([FIRST, THIRD], SING)))
add_tok(VerbPass('were', PRET, nom_subj_pat(SECOND, SING)))
add_tok(VerbPass('were', PRET, nom_subj_pat(ANY, PLUR)))
add_tok(VerbPassInter('am', PRES, nom_subj_pat(FIRST, SING)))
add_tok(VerbPassInter('\'m', PRES, nom_subj_pat(FIRST, SING)))
add_tok(VerbPassInter('are', PRES, nom_subj_pat(ANY, PLUR)))
add_tok(VerbPassInter('\'re', PRES, nom_subj_pat(ANY, PLUR)))
add_tok(VerbPassInter('are', PRES, nom_subj_pat(SECOND, SING)))
add_tok(VerbPassInter('is', PRES, nom_subj_pat(THIRD, SING)))
add_tok(VerbPassInter('was', PRET, nom_subj_pat([FIRST, THIRD], SING)))
add_tok(VerbPassInter('were', PRET, nom_subj_pat(SECOND, SING)))
add_tok(VerbPassInter('were', PRET, nom_subj_pat(SECOND, PLUR)))
add_tok(VerbPass('been', PART, nom_subj_pat_any))
add_tok(VerbPass('being', GERUND, nom_subj_pat_any))
add_tok(VerbPass('be', BARE, nom_subj_pat_any))

have_aux_arg_pats = [{CAT: VP, FORM: PART, HAS_SUBJ: False}]
add_tok(Verb('have', [PRES, BARE], nom_subj_pat_any, have_aux_arg_pats))
add_tok(Verb('\'ve', PRES, nom_subj_pat_any, have_aux_arg_pats))
add_tok(Verb('has', PRES, nom_subj_pat(THIRD, SING), have_aux_arg_pats))
add_tok(Verb('\'s', PRES, nom_subj_pat(THIRD, SING), have_aux_arg_pats))
add_tok(Verb('had', PRET, nom_subj_pat_any, have_aux_arg_pats))
add_tok(Verb('\'d', PRET, nom_subj_pat_any, have_aux_arg_pats))

inf_arg_pat = {CAT: CP, LEX: 'to'}
add_tok(Complementizer('to', {FORM: BARE, HAS_SUBJ: False}))

add_tok(Complementizer('that', {FORM: [PRES, PRET, MODAL], HAS_SUBJ: True}))

# Modals
modal_arg_pats = [{CAT: VP, FORM: BARE, HAS_SUBJ: False}]
add_tok(Verb('can', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(Verb('could', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(Verb('shall', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(Verb('should', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(Verb('will', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(Verb('\'ll', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(Verb('would', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(Verb('may', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(Verb('might', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(Verb('must', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('can', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('could', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('shall', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('should', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('will', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('\'ll', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('would', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('may', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('might', MODAL, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('must', MODAL, nom_subj_pat_any, modal_arg_pats))

add_tok(Verb('do', PRES, [nom_subj_pat([FIRST, SECOND], SING), nom_subj_pat(ANY, PLUR)], modal_arg_pats))
add_tok(Verb('does', PRES, nom_subj_pat(THIRD, SING), modal_arg_pats))
add_tok(Verb('did', PRET, nom_subj_pat_any, modal_arg_pats))
add_tok(VerbInter('do', PRES, [nom_subj_pat([FIRST, SECOND], SING), nom_subj_pat(ANY, PLUR)], modal_arg_pats))
add_tok(VerbInter('does', PRES, nom_subj_pat(THIRD, SING), modal_arg_pats))
add_tok(VerbInter('did', PRET, nom_subj_pat_any, modal_arg_pats))
dp_arg_pat = {CAT: DP, CASE: ACC}
add_tok(Verb('do', PRES, [nom_subj_pat([FIRST, SECOND], SING), nom_subj_pat(ANY, PLUR)], [dp_arg_pat]))
add_tok(Verb('does', PRES, nom_subj_pat(THIRD, SING), [dp_arg_pat]))
add_tok(Verb('did', PRET, nom_subj_pat_any, [dp_arg_pat]))
add_tok(Verb('done', PART, nom_subj_pat_any, [dp_arg_pat]))
add_tok(Verb('doing', GERUND, nom_subj_pat_any, [dp_arg_pat]))

dest_arg_pat = {CAT: PP, LEX: 'to'}
add_tok(Verb('go', PRES, [nom_subj_pat([FIRST, SECOND], SING), nom_subj_pat(ANY, PLUR)], [dest_arg_pat]))
add_tok(Verb('goes', PRES, nom_subj_pat(THIRD, SING), [dest_arg_pat]))
add_tok(Verb('went', PRET, nom_subj_pat_any, [dest_arg_pat]))
add_tok(Verb('gone', PART, nom_subj_pat_any, [dest_arg_pat]))
add_tok(Verb('going', GERUND, nom_subj_pat_any, [dest_arg_pat]))
add_tok(Verb('going', GERUND, nom_subj_pat_any, [inf_arg_pat]))

add_tok(PrepositionMod('with', {CAT: VP}))
add_tok(PrepositionMod('by', {CAT: VP, FORM: PART}))
add_tok(Preposition('to'))