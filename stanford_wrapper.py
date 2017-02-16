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

def parse(text):
  tokenized = MaxentTagger.tokenizeText(StringReader(text))
  it = tokenized.iterator()
  parsed = []
  while it.hasNext():
    tokenized_sent = it.next()
    tagged_sent = tagger.tagSentence(tokenized_sent)
    gs = parser.predict(tagged_sent)
    td_it = gs.typedDependencies().iterator()
    deps = []
    while td_it.hasNext():
      td = td_it.next()
      deps.append(
        ((td.gov().word(), td.gov().index()), td.reln().getShortName(), (td.dep().word(), td.dep().index()))
      )
    parsed.append(deps)
  return parsed

