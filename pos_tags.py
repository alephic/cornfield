from util import multidict_add

def acc_pos_tags(conllu_filename):
  all_tags = {}
  with open(conllu_filename) as f:
    for line in f:
      if line.startswith('#') or line == '\n':
        continue
      else:
        cols = line.rstrip('\n').split('\t')
        multidict_add(all_tags, cols[1].lower(), cols[4])
  return all_tags

