from tags import *
from vocab import *

def lam_apply(l_edgess, r_edgess, fringe_entry):
  (l_i, r_i, item) = fringe_entry
  if l_i-1 > 0:
    for (far_l_i, l_item) in r_edgess[l_i-1]:
      if l_item.bilam and far_l_i-1 > 0:
        for (further_l_i, far_l_item) in r_edgess[far_l_i-1]:
          res_bi_l = l_item.bilam(l_item, far_l_item, item)
          if res_bi_l:
            yield (further_l_i, r_i, res_bi_l)
      res_l = l_item.rlam(l_item, item)
      if res_l:
        yield (far_l_i, r_i, res_l)
      res = item.llam(item, l_item)
      if res:
        yield (far_l_i, r_i, res)
  if r_i+1 < len(l_edgess):
    for (far_r_i, r_item) in l_edgess[r_i+1]:
      if r_item.bilam and far_r_i+1 < len(l_edgess):
        for (further_r_i, far_r_item) in l_edgess[far_r_i+1]:
          res_bi_r = r_item.bilam(r_item, item, far_r_item)
          if res_bi_r:
            yield (l_i, further_r_i, res_bi_r)
      res_r = r_item.llam(r_item, item)
      if res_r:
        yield (l_i, far_r_i, res_r)
      res = item.rlam(item, r_item)
      if res:
        yield (l_i, far_r_i, res)
    if item.bilam and l_i-1 > 0:
      for (far_l_i, l_item) in r_edgess[l_i-1]:
        for (far_r_i, r_item) in l_edgess[r_i+1]:
          res_bi = item.bilam(item, l_item, r_item)
          if res_bi:
            yield (far_l_i, far_r_i, res_bi)

def parse_tokens(tokenss, verbose=False):
  l_edgess = [[] for i in range(len(tokenss))]
  r_edgess = [[] for i in range(len(tokenss))]
  fringe = [(i, i, t) for i in range(len(tokenss)) for t in tokenss[i]]
  while len(fringe) > 0:
    (l_i, r_i, item) = fringe_entry = fringe.pop()
    print("Popped", fringe_entry)
    if l_i == 0 and r_i == len(tokenss)-1:
      yield item
      continue
    l_edgess[l_i].append((r_i, item))
    r_edgess[r_i].append((l_i, item))
    for new_entry in lam_apply(l_edgess, r_edgess, fringe_entry):
      (new_l_i, new_r_i, new_item) = new_entry
      fringe.append(new_entry)

def tokenize(text):
  res = []
  for chunk in text.split(' '):
    has_pf = False
    for pf in postfixes:
      if chunk.endswith(pf):
        res.append(chunk[:-len(pf)])
        res.append(pf)
        has_pf = True
        break
    if not has_pf:
      res.append(chunk)
  return res

def tag(text):
  return [get_tags(word.lower()) for word in tokenize(text)]

def parse(text):
  return next(parse_tokens(tag(text)), None)