
# Copyright (c) 2017, Brendon Matusch. All rights reserved.

import glob
import os

pngList = glob.glob("./*.png")

num = len(pngList)

numList = []

for i in range(num):
    numList.append(pngList[i][4:-4])

numList.sort(key=int)

with open('valnum.txt', 'w') as f:
    for j in range(num):
        f.write(str(numList[j]))
        f.write('\n')
