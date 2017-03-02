import os
array = []
with open('_Data.txt') as f:
    for line in f:
        array.append(line.rstrip('\n'))
for i in range(1, 2142):
    os.rename('HalfApple (' + str(i) + ').png', array[i - 1] + '-' + str(i) + '.png')
