from util import multidict_add
import pickle

def acc_pos_tags(conllu_filename):
  all_tags = {}
  with open(conllu_filename) as f:
    for line in f:
      if line.startswith('#') or line == '\n':
        continue
      else:
        cols = line.rstrip('\n').split('\t')
        lex = cols[1].lower()
        pos = cols[4]
        if lex in all_tags:
          if pos not in all_tags[lex]:
            all_tags[lex].append(pos)
        else:
          all_tags[lex] = [pos]
  return all_tags

def dump_pos_tags(conllu_filename, dest_filename):
  with open(dest_filename, mode='wb') as dest:
    tags = acc_pos_tags(conllu_filename)
    pickle.dump(tags, dest)

def load_pos_tags(dumped_filename):
  loaded = None
  with open(dumped_filename, mode='rb') as dumped:
    loaded = pickle.load(dumped)
  return loaded