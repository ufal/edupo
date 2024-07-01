import random

#set seed
random.seed(123)

with open('train_all.txt') as f:
    lines = f.readlines()

#create validation sets with 90 % of lines

random.shuffle(lines)

for i in range(10):
    with open('train_' + str(i) + '.txt', 'w') as f:
        with open('val_' + str(i) + '.txt', 'w') as f_val:
            # leave out 10 % of the lines
            for j, line in enumerate(lines):
                if j % 10 == i:
                    f_val.write(line)
                f.write(line)    
    
