
def multidict_add(d, k, v):
  if k in d:
    d[k].append(v)
  else:
    d[k] = [v]

class DefaultDict(dict):
  def __init__(self, default):
    self.default = default
  def __getitem__(self, item):
    return super().__getitem__(item) if item in self else self.default