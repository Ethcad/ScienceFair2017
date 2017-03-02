
# Copyright (c) 2017, Brendon Matusch. All rights reserved
# StatisticallyAccurateRounding.py

# This script is intended to be used on averaged data from multiple human classifications of fruit. It rounds each line to an integer as normal, except that 50% of values ending in .5 are rounded down instead of up.

import os
array = []
with open('Input.txt') as f:
    for line in f:
        array.append(line.rstrip('\n'))
r = open('Output.txt', 'w')
pt5Toggle = 0
for j in range(1, 489):
    i = j - 1
    if (array[i])[-2:] == ".5":
        r.write(str(int(round(float(array[i]) + (pt5Toggle - 0.5)))))
        if pt5Toggle == 0:
            pt5Toggle = 1
        else:
            pt5Toggle = 0
    else:
        r.write(str(int(round(float(array[i])))))
    r.write('\n')
