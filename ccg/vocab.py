from util import multidict_add
from tags import *
import pos_tags

known_tags = {}
postfixes = ['\'', '\'s', '\'ve', '\'d', '\'m', '\'re', '\'ll', 'n\'t', ',', '.', '?', '!']

known_pos = pos_tags.load_pos_tags('en-ud-tags.pkl')

def morph_detect(lex):
  if lex.endswith('ed'):
    return ['VBD', 'VBN']
  elif lex.endswith('ing'):
    return ['VBG']
  elif lex.endswith('s'):
    return ['VBZ', 'NNS']
  elif lex.endswith('ly'):
    return ['RB']
  else:
    return ['VB', 'VBP', 'NN', 'NNP', 'JJ']


def get_tags(lex):
  if lex in known_tags:
    return known_tags[lex]
  else:
    poss = None
    if lex in known_pos:
      poss = known_pos[lex]
    else:
      poss = morph_detect(lex)
    res = []
    for pos in poss:
      res.extend(guess_tags(lex, pos))
    return res

def guess_tags(lex, pos):
  if pos == 'NN':
    return [Noun(lex, SING), FeatToken(lex, {CAT: DP, CASE: ANY, COUNT: SING, PERSON: THIRD})]
  elif pos == 'NNS':
    return [Noun(lex, PLUR), FeatToken(lex, {CAT: DP, CASE: ANY, COUNT: PLUR, PERSON: THIRD})]
  elif pos == 'NNP':
    return [FeatToken(lex, {CAT: DP, CASE: ANY, COUNT: SING, PERSON: THIRD})]
  elif pos == 'NNPS':
    return [FeatToken(lex, {CAT: DP, CASE: ANY, COUNT: PLUR, PERSON: THIRD})]
  elif pos == 'JJ':
    return [PosAdjective(lex)]
  elif pos == 'JJR':
    return [CmpAdjective(lex)]
  elif pos == 'RB':
    return [Adverb(lex)]
  elif pos == 'VB':
    return [Verb(lex, BARE, nom_subj_pat_any, [dp_arg_pat])]
  elif pos == 'VBP':
    return [Verb(lex, PRES, nom_subj_pat_nontps, [dp_arg_pat])]
  elif pos == 'VBZ':
    return [Verb(lex, PRES, nom_subj_pat_tps, [dp_arg_pat])]
  elif pos == 'VBD':
    return [Verb(lex, PRET, nom_subj_pat_any, [dp_arg_pat])]
  elif pos == 'VBN':
    return [Verb(lex, PART, nom_subj_pat_any, [dp_arg_pat])]
  elif pos == 'VBG':
    return [Verb(lex, GERUND, nom_subj_pat_any, [dp_arg_pat])]
  elif pos == 'IN':
    return [PrepositionMod(lex, {CAT: [VP, DP]}), ComplementizerMod(lex, {CAT: VP}, [{FORM: [PRET, PRES]}, {HAS_SUBJ: False, FORM: GERUND}])]
  else:
    return []

def add_tok(tok):
  multidict_add(known_tags, tok.lex, tok)

def add_verb_default(lex, arg_pats):
  add_tok(Verb(lex, BARE, nom_subj_pat_any, arg_pats))
  add_tok(Verb(lex, PRES, nom_subj_pat_nontps, arg_pats))
  add_tok(Verb(lex+'s', PRES, nom_subj_pat_tps, arg_pats))
  add_tok(Verb(lex+'d' if lex.endswith('e') else lex+'ed', [PRET, PART], nom_subj_pat_any, arg_pats))
  add_tok(Verb(lex+'ing', GERUND, nom_subj_pat_any, arg_pats))
  
add_tok(Conjunction('and'))
add_tok(Conjunction('or'))

add_tok(Possessive('\'s'))
add_tok(Possessive('\''))
add_tok(PrepositionMod('of', {CAT: N}))

add_tok(Determiner('the', ANY))
add_tok(Determiner('a', SING))
add_tok(Determiner('an', SING))

add_tok(Pronoun('i', SING, NOM, FIRST))
add_tok(Pronoun('me', SING, ACC, FIRST))
add_tok(Pronoun('myself', SING, ACC, FIRST))
add_tok(Determiner('my', ANY))
add_tok(Pronoun('mine', ANY, ANY, THIRD))
add_tok(Pronoun('we', PLUR, NOM, FIRST))
add_tok(Pronoun('us', PLUR, ACC, FIRST))
add_tok(Pronoun('ourselves', PLUR, ACC, FIRST))
add_tok(Determiner('our', ANY))
add_tok(Pronoun('ours', ANY, ANY, THIRD))
add_tok(Pronoun('you', ANY, ANY, SECOND))
add_tok(Pronoun('yourself', SING, ACC, SECOND))
add_tok(Pronoun('yourselves', PLUR, ACC, SECOND))
add_tok(Determiner('your', ANY))
add_tok(Pronoun('yours', ANY, ANY, THIRD))
add_tok(Pronoun('he', SING, NOM, THIRD))
add_tok(Pronoun('him', SING, ACC, THIRD))
add_tok(Pronoun('himself', SING, ACC, THIRD))
add_tok(Determiner('his', ANY))
add_tok(Pronoun('his', ANY, ANY, THIRD))
add_tok(Pronoun('she', SING, NOM, THIRD))
add_tok(Pronoun('her', SING, ACC, THIRD))
add_tok(Pronoun('herself', SING, ACC, THIRD))
add_tok(Determiner('her', ANY))
add_tok(Pronoun('hers', ANY, ANY, THIRD))
add_tok(Pronoun('it', SING, ANY, THIRD))
add_tok(Pronoun('itself', SING, ACC, THIRD))
add_tok(Determiner('its', ANY))
add_tok(Pronoun('its', ANY, ANY, THIRD))
add_tok(Pronoun('they', PLUR, NOM, THIRD))
add_tok(Pronoun('them', PLUR, ACC, THIRD))
add_tok(Pronoun('themselves', PLUR, ACC, THIRD))
add_tok(Determiner('their', ANY))
add_tok(Pronoun('theirs', ANY, ANY, THIRD))
add_tok(Pronoun('that', SING, ANY, THIRD, rel=True))
add_tok(Determiner('that', SING))
add_tok(Pronoun('those', PLUR, ANY, THIRD))
add_tok(Determiner('those', PLUR))
add_tok(Pronoun('this', SING, ANY, THIRD))
add_tok(Determiner('this', SING))
add_tok(Pronoun('these', PLUR, ANY, THIRD))
add_tok(Determiner('these', PLUR))

add_tok(Pronoun('what', ANY, ANY, THIRD, rel=REL_EXT))
add_tok(Pronoun('who', ANY, ANY, THIRD, rel=REL_EXT))
add_tok(Pronoun('where', ANY, ANY, THIRD, rel=REL_EXT, loc=True))
add_tok(Pronoun('which', ANY, ANY, THIRD, rel=REL_EXT))
add_tok(Complementizer('why', {CAT: VP, FORM: [PRES, PRET]}))
add_tok(Pronoun('whom', ANY, ACC, THIRD, rel=REL_EXT))
whose_tok = Determiner('whose', ANY)
whose_tok.feats[REL] = REL_EXT
add_tok(whose_tok)
cond_arg_pat = {CAT: VP, FORM: [PRES, PRET, MODAL]}
add_tok(ComplementizerMod('when', {CAT: VP}, cond_arg_pat))
add_tok(ComplementizerMod('if', {CAT: VP}, cond_arg_pat))
add_tok(ComplementizerMod('while', {CAT: VP}, cond_arg_pat))

reason_rlam = get_basic_arg_rlam({CAT: CP, LEX: ['why', 'that']})
add_tok(FeatToken('reason', {CAT: N, COUNT: SING}, rlam=reason_rlam))
add_tok(FeatToken('reasons', {CAT: N, COUNT: PLUR}, rlam=reason_rlam))

fact_rlam = get_basic_arg_rlam({CAT: CP, LEX: 'that'})
add_tok(FeatToken('fact', {CAT: N, COUNT: SING}, rlam=fact_rlam))
add_tok(FeatToken('facts', {CAT: N, COUNT: PLUR}, rlam=fact_rlam))
add_tok(FeatToken('idea', {CAT: N, COUNT: SING}, rlam=fact_rlam))
add_tok(FeatToken('ideas', {CAT: N, COUNT: PLUR}, rlam=fact_rlam))
add_tok(FeatToken('proposition', {CAT: N, COUNT: SING}, rlam=fact_rlam))
add_tok(FeatToken('propositions', {CAT: N, COUNT: PLUR}, rlam=fact_rlam))
add_tok(FeatToken('statement', {CAT: N, COUNT: SING}, rlam=fact_rlam))
add_tok(FeatToken('statements', {CAT: N, COUNT: PLUR}, rlam=fact_rlam))
add_tok(FeatToken('claim', {CAT: N, COUNT: SING}, rlam=fact_rlam))
add_tok(FeatToken('claims', {CAT: N, COUNT: PLUR}, rlam=fact_rlam))
add_tok(FeatToken('argument', {CAT: N, COUNT: SING}, rlam=fact_rlam))
add_tok(FeatToken('arguments', {CAT: N, COUNT: PLUR}, rlam=fact_rlam))

add_tok(Pronoun('there', SING, ANY, THIRD, loc=True))

add_tok(FeatToken('one', {CAT: DP, CASE: ANY, COUNT: SING, PERSON: THIRD, CAN_REL: True}))
add_tok(FeatToken('one', {CAT: N, COUNT: SING}))

add_tok(FeatToken('something', {CAT: DP, CASE: ANY, COUNT: SING, PERSON: THIRD, CAN_REL: True}))
add_tok(FeatToken('somewhere', {CAT: DP, CASE: ANY, COUNT: SING, PERSON: THIRD, LOC: True}))

copula_arg_pats = [[{CAT: [Adj, PP]}, {CAT: DP, CASE: ACC, COUNT: ANY}]]
# Copular verb
add_tok(Verb('am', PRES, nom_subj_pat(FIRST, SING), copula_arg_pats))
add_tok(Verb('\'m', PRES, nom_subj_pat(FIRST, SING), copula_arg_pats))
add_tok(Verb('are', PRES, nom_subj_pat(ANY, PLUR), copula_arg_pats))
add_tok(Verb('\'re', PRES, nom_subj_pat(ANY, PLUR), copula_arg_pats))
add_tok(Verb('are', PRES, nom_subj_pat(SECOND, SING), copula_arg_pats))
add_tok(Verb('is', PRES, nom_subj_pat_tps, copula_arg_pats))
add_tok(Verb('\'s', PRES, nom_subj_pat_tps, copula_arg_pats))
add_tok(Verb('was', PRET, nom_subj_pat([FIRST, THIRD], SING), copula_arg_pats))
add_tok(Verb('were', PRET, nom_subj_pat(SECOND, SING), copula_arg_pats))
add_tok(Verb('were', PRET, nom_subj_pat(ANY, PLUR), copula_arg_pats))
add_tok(VerbInter('am', PRES, nom_subj_pat(FIRST, SING), copula_arg_pats))
add_tok(VerbInter('\'m', PRES, nom_subj_pat(FIRST, SING), copula_arg_pats))
add_tok(VerbInter('are', PRES, nom_subj_pat(ANY, PLUR), copula_arg_pats))
add_tok(VerbInter('\'re', PRES, nom_subj_pat(ANY, PLUR), copula_arg_pats))
add_tok(VerbInter('are', PRES, nom_subj_pat(SECOND, SING), copula_arg_pats))
add_tok(VerbInter('is', PRES, nom_subj_pat_tps, copula_arg_pats))
add_tok(VerbInter('was', PRET, nom_subj_pat([FIRST, THIRD], SING), copula_arg_pats))
add_tok(VerbInter('were', PRET, nom_subj_pat(SECOND, SING), copula_arg_pats))
add_tok(VerbInter('were', PRET, nom_subj_pat(SECOND, PLUR), copula_arg_pats))
add_tok(Verb('been', PART, nom_subj_pat_any, copula_arg_pats))
add_tok(Verb('being', GERUND, nom_subj_pat_any, copula_arg_pats))
add_tok(Verb('be', BARE, nom_subj_pat_any, copula_arg_pats))

# Passive verb
add_tok(VerbPass('am', PRES, nom_subj_pat(FIRST, SING)))
add_tok(VerbPass('\'m', PRES, nom_subj_pat(FIRST, SING)))
add_tok(VerbPass('are', PRES, nom_subj_pat(ANY, PLUR)))
add_tok(VerbPass('\'re', PRES, nom_subj_pat(ANY, PLUR)))
add_tok(VerbPass('are', PRES, nom_subj_pat(SECOND, SING)))
add_tok(VerbPass('is', PRES, nom_subj_pat_tps))
add_tok(VerbPass('\'s', PRES, nom_subj_pat_tps))
add_tok(VerbPass('was', PRET, nom_subj_pat([FIRST, THIRD], SING)))
add_tok(VerbPass('were', PRET, nom_subj_pat(SECOND, SING)))
add_tok(VerbPass('were', PRET, nom_subj_pat(ANY, PLUR)))
add_tok(VerbPassInter('am', PRES, nom_subj_pat(FIRST, SING)))
add_tok(VerbPassInter('\'m', PRES, nom_subj_pat(FIRST, SING)))
add_tok(VerbPassInter('are', PRES, nom_subj_pat(ANY, PLUR)))
add_tok(VerbPassInter('\'re', PRES, nom_subj_pat(ANY, PLUR)))
add_tok(VerbPassInter('are', PRES, nom_subj_pat(SECOND, SING)))
add_tok(VerbPassInter('is', PRES, nom_subj_pat_tps))
add_tok(VerbPassInter('was', PRET, nom_subj_pat([FIRST, THIRD], SING)))
add_tok(VerbPassInter('were', PRET, nom_subj_pat(SECOND, SING)))
add_tok(VerbPassInter('were', PRET, nom_subj_pat(SECOND, PLUR)))
add_tok(VerbPass('been', PART, nom_subj_pat_any))
add_tok(VerbPass('being', GERUND, nom_subj_pat_any))
add_tok(VerbPass('be', BARE, nom_subj_pat_any))

gerund_arg_pat = {FORM: GERUND}

# Gerund auxiliary verb
add_tok(VerbAux('am', PRES, nom_subj_pat(FIRST, SING), gerund_arg_pat))
add_tok(VerbAux('\'m', PRES, nom_subj_pat(FIRST, SING), gerund_arg_pat))
add_tok(VerbAux('are', PRES, nom_subj_pat(ANY, PLUR), gerund_arg_pat))
add_tok(VerbAux('\'re', PRES, nom_subj_pat(ANY, PLUR), gerund_arg_pat))
add_tok(VerbAux('are', PRES, nom_subj_pat(SECOND, SING), gerund_arg_pat))
add_tok(VerbAux('is', PRES, nom_subj_pat_tps, gerund_arg_pat))
add_tok(VerbAux('\'s', PRES, nom_subj_pat_tps, gerund_arg_pat))
add_tok(VerbAux('was', PRET, nom_subj_pat([FIRST, THIRD], SING), gerund_arg_pat))
add_tok(VerbAux('were', PRET, nom_subj_pat(SECOND, SING), gerund_arg_pat))
add_tok(VerbAux('were', PRET, nom_subj_pat(ANY, PLUR), gerund_arg_pat))
add_tok(VerbAuxInter('am', PRES, nom_subj_pat(FIRST, SING), gerund_arg_pat))
add_tok(VerbAuxInter('\'m', PRES, nom_subj_pat(FIRST, SING), gerund_arg_pat))
add_tok(VerbAuxInter('are', PRES, nom_subj_pat(ANY, PLUR), gerund_arg_pat))
add_tok(VerbAuxInter('\'re', PRES, nom_subj_pat(ANY, PLUR), gerund_arg_pat))
add_tok(VerbAuxInter('are', PRES, nom_subj_pat(SECOND, SING), gerund_arg_pat))
add_tok(VerbAuxInter('is', PRES, nom_subj_pat_tps, gerund_arg_pat))
add_tok(VerbAuxInter('was', PRET, nom_subj_pat([FIRST, THIRD], SING), gerund_arg_pat))
add_tok(VerbAuxInter('were', PRET, nom_subj_pat(SECOND, SING), gerund_arg_pat))
add_tok(VerbAuxInter('were', PRET, nom_subj_pat(SECOND, PLUR), gerund_arg_pat))
add_tok(VerbAux('been', PART, nom_subj_pat_any, gerund_arg_pat))
add_tok(VerbAux('being', GERUND, nom_subj_pat_any, gerund_arg_pat))
add_tok(VerbAux('be', BARE, nom_subj_pat_any, gerund_arg_pat))

# Perfect auxiliary verb
perf_aux_arg_pat = {FORM: PART}
add_tok(VerbAux('have', BARE, nom_subj_pat_any, perf_aux_arg_pat))
add_tok(VerbAux('\'ve', BARE, nom_subj_pat_any, perf_aux_arg_pat))
add_tok(VerbAux('have', PRES, nom_subj_pat_nontps, perf_aux_arg_pat))
add_tok(VerbAux('\'ve', PRES, nom_subj_pat_nontps, perf_aux_arg_pat))
add_tok(VerbAux('has', PRES, nom_subj_pat_tps, perf_aux_arg_pat))
add_tok(VerbAux('\'s', PRES, nom_subj_pat_tps, perf_aux_arg_pat))
add_tok(VerbAux('had', PRET, nom_subj_pat_any, perf_aux_arg_pat))
add_tok(VerbAux('\'d', PRET, nom_subj_pat_any, perf_aux_arg_pat))
add_tok(VerbAuxInter('have', BARE, nom_subj_pat_any, perf_aux_arg_pat))
add_tok(VerbAuxInter('\'ve', BARE, nom_subj_pat_any, perf_aux_arg_pat))
add_tok(VerbAuxInter('have', PRES, nom_subj_pat_nontps, perf_aux_arg_pat))
add_tok(VerbAuxInter('\'ve', PRES, nom_subj_pat_nontps, perf_aux_arg_pat))
add_tok(VerbAuxInter('has', PRES, nom_subj_pat_tps, perf_aux_arg_pat))
add_tok(VerbAuxInter('\'s', PRES, nom_subj_pat_tps, perf_aux_arg_pat))
add_tok(VerbAuxInter('had', PRET, nom_subj_pat_any, perf_aux_arg_pat))
add_tok(VerbAuxInter('\'d', PRET, nom_subj_pat_any, perf_aux_arg_pat))

add_tok(VerbAux('to', INF, nom_subj_pat_any, {FORM: BARE}))

inf_arg_pat = {FORM: INF}
# Necessitative "have"
add_tok(VerbAux('have', BARE, nom_subj_pat_any, inf_arg_pat))
add_tok(VerbAux('\'ve', BARE, nom_subj_pat_any, inf_arg_pat))
add_tok(VerbAux('have', PRES, nom_subj_pat_nontps, inf_arg_pat))
add_tok(VerbAux('\'ve', PRES, nom_subj_pat_nontps, inf_arg_pat))
add_tok(VerbAux('has', PRES, nom_subj_pat_tps, inf_arg_pat))
add_tok(VerbAux('\'s', PRES, nom_subj_pat_tps, inf_arg_pat))
add_tok(VerbAux('had', PRET, nom_subj_pat_any, inf_arg_pat))
add_tok(VerbAux('\'d', PRET, nom_subj_pat_any, inf_arg_pat))

add_tok(Complementizer('that', {FORM: [PRES, PRET, MODAL], HAS_SUBJ: True}))

# Modals
modal_arg_pat = {FORM: BARE}
add_tok(VerbAux('can', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAux('ca', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAux('could', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAux('shall', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAux('should', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAux('will', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAux('\'ll', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAux('would', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAux('may', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAux('might', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAux('must', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('can', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('ca', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('could', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('shall', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('should', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('will', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('\'ll', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('would', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('may', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('might', MODAL, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('must', MODAL, nom_subj_pat_any, modal_arg_pat))

add_tok(VerbAux('do', [PRES, BARE], nom_subj_pat_nontps, modal_arg_pat))
add_tok(VerbAux('does', PRES, nom_subj_pat_tps, modal_arg_pat))
add_tok(VerbAux('did', PRET, nom_subj_pat_any, modal_arg_pat))
add_tok(VerbAuxInter('do', [PRES, BARE], nom_subj_pat_nontps, modal_arg_pat))
add_tok(VerbAuxInter('does', PRES, nom_subj_pat_tps, modal_arg_pat))
add_tok(VerbAuxInter('did', PRET, nom_subj_pat_any, modal_arg_pat))
dp_arg_pat = {CAT: DP, CASE: ACC}
add_tok(Verb('do', [PRES, BARE], nom_subj_pat_nontps, [dp_arg_pat]))
add_tok(Verb('does', PRES, nom_subj_pat_tps, [dp_arg_pat]))
add_tok(Verb('did', PRET, nom_subj_pat_any, [dp_arg_pat]))
add_tok(Verb('done', PART, nom_subj_pat_any, [dp_arg_pat]))
add_tok(Verb('doing', GERUND, nom_subj_pat_any, [dp_arg_pat]))

dest_arg_pat = [{CAT: PP, LEX: 'to'}, {CAT: DP, CASE: ACC, LOC: True}]
add_tok(Verb('go', [PRES, BARE], nom_subj_pat_nontps, [dest_arg_pat]))
add_tok(Verb('goes', PRES, nom_subj_pat_tps, [dest_arg_pat]))
add_tok(Verb('went', PRET, nom_subj_pat_any, [dest_arg_pat]))
add_tok(Verb('gone', PART, nom_subj_pat_any, [dest_arg_pat]))
add_tok(Verb('going', GERUND, nom_subj_pat_any, [dest_arg_pat]))

# Informal future
add_tok(VerbAux('going', GERUND, nom_subj_pat_any, inf_arg_pat))
add_tok(VerbAux('gonna', GERUND, nom_subj_pat_any, {FORM: BARE}))
# Repetitive past
add_tok(VerbAux('used', PRET, nom_subj_pat_any, inf_arg_pat))
# Use
add_verb_default('use', [dp_arg_pat, {CAT: VP, FORM: INF}])

req_arg_pats = [[dp_arg_pat, {CAT: VP, FORM: INF}]]
# Want
add_verb_default('want', req_arg_pats)
add_tok(VerbAux('wanna', PRES, nom_subj_pat_nontps, {FORM: BARE}))
add_tok(VerbAux('wanna', BARE, nom_subj_pat_any, {FORM: BARE}))
# Need
add_verb_default('need', req_arg_pats)

# Become
add_tok(Verb('become', BARE, nom_subj_pat_any, copula_arg_pats))
add_tok(Verb('become', PRES, nom_subj_pat_nontps, copula_arg_pats))
add_tok(Verb('becomes', PRES, nom_subj_pat_tps, copula_arg_pats))
add_tok(Verb('become', PART, nom_subj_pat_any, copula_arg_pats))
add_tok(Verb('became', PRET, nom_subj_pat_any, copula_arg_pats))
add_tok(Verb('becoming', GERUND, nom_subj_pat_any, copula_arg_pats))
add_tok(VerbPass('become', BARE, nom_subj_pat_any))
add_tok(VerbPass('become', PRES, nom_subj_pat_nontps))
add_tok(VerbPass('becomes', PRES, nom_subj_pat_tps))
add_tok(VerbPass('become', PART, nom_subj_pat_any))
add_tok(VerbPass('became', PRET, nom_subj_pat_any))
add_tok(VerbPass('becoming', GERUND, nom_subj_pat_any))

add_tok(PrepositionMod('with', {CAT: [VP, DP]}))
add_tok(PrepositionMod('by', {CAT: V, FORM: PART}))
add_tok(Preposition('to'))

add_tok(Preposition('than'))

report_arg_pats = [[{CAT: DP, CASE: ACC}]]