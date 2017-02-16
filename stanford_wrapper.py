import os

stanford_dir = "stanford-parser-full-2016-10-31"

os.environ['CLASSPATH'] = stanford_dir+"/*"

from jnius import autoclass

DependencyParser = autoclass('edu.stanford.nlp.parser.nndep.DependencyParser')
MaxentTagger = autoclass('edu.stanford.nlp.tagger.maxent.MaxentTagger')
print('Loading tagger...')
tagger = MaxentTagger('edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger')

print('Loading parser...')
parser = DependencyParser.loadFromModelFile('edu/stanford/nlp/models/parser/nndep/english_UD.gz')

StringReader = autoclass('java.io.StringReader')

class DepList(list):
  def __repr__(self):
    return '\n'.join(map(lambda t: str(t[0])+': '+', '.join(map(repr, t[1])), zip(range(len(self)), self)))

def parse(text):
  tokenized = MaxentTagger.tokenizeText(StringReader(text))
  it = tokenized.iterator()
  parsed = []
  while it.hasNext():
    tokenized_sent = it.next()
    tagged_sent = tagger.tagSentence(tokenized_sent)
    words = DepList()
    words.append(('ROOT', 'ROOT', -1, None))
    tg_it = tagged_sent.iterator()
    while tg_it.hasNext():
      tg = tg_it.next()
      words.append((tg.word(), tg.tag()))
    gs = parser.predict(tagged_sent)
    td_it = gs.typedDependencies().iterator()
    deps = []
    while td_it.hasNext():
      td = td_it.next()
      wt = words[td.dep().index()]
      words[td.dep().index()] = (wt[0], wt[1], td.gov().index(), td.reln().getShortName())
    parsed.append(words)
  return parsed