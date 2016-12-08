
def multidict_add(d, k, v):
  if k in d:
    d[k].append(v)
  else:
    d[k] = [v]
