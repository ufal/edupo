import sys

from hyphenator import Hyphenator

#out_only = True
out_only = False

with open(sys.argv[1], 'r') as f:
    patterns = f.read().splitlines()

with open(sys.argv[2], 'r') as f:
    data = f.read().splitlines()

hyp = Hyphenator(patterns)

correct = 0
incorrect = 0
for word in data:
    test = ''.join(x for x in word if x != '-')
    test_out = '-'.join(hyp.hyphenate_word(test))
    if out_only:
        print(test_out)
    else:
        if test_out == word:
            correct += 1
        else:
            print(test, test_out, word)
            incorrect += 1
if not out_only:
    print(f'Correct: {correct}, Incorrect: {incorrect}, Accuracy: {correct / (correct + incorrect)}')
