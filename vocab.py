
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
adjs_infl = {
  'good':('better','best'),
  'bad':('worse','worst')
}
def get_adj_degrees(adj):
  if adj in adjs_infl:
    return adjs_infl[adj]
  else:
    root = adj + adj[-1] if adj[-2:] in ['in','ig','at','an','ad'] else adj
    root = root + 'e' if root[-1] != 'e' else root
    return (root+'r',root+'st')
