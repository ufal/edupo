import sys
from rhymetagger import RhymeTagger

# read poem
poem = []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if line:
            poem.append(line)
f.close()

rt = RhymeTagger()

# Slots to hold current stanza and poem id
rt.stanza_id = 0
rt.poem_id = 0

# Container for dataset. Items correspond to a single line
# and hold a tuple (rhyme_word, poem_id, stanza_id)
rt.data = list()
        
# Container for vocabulary. Each key is a rhyme_word found in
# the dataset and holds a tuple ([components], final_ngram)
rt.rhyme_vocab = dict()     

# Perform tagging        
rt.verbose = False        

# Parameters
rt.transcribed = False        
rt.lang = "cs"
rt.vowel_length = False
rt.stress = True
rt.syll_max = 2
rt.ngram_length = 10

rt.add_to_model(poem)

if len(poem) != len(rt.data):
    sys.stderr.write("Error: Line counts don't match!\n")
else:
    for i, line in enumerate(rt.data):
        components = rt.rhyme_vocab[line[0]][0]
        print(poem[i], list(reversed(components)))

