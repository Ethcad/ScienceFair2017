
# Copyright (c) 2017, Brendon Matusch. All rights reserved.
# ParseRawOutput.py

# This script parses raw output from a PyCaffe neural network application script and converts it to a simple list of the top classifications for each image.

import os

with open("rawoutput.txt", "r") as f:
    data = f.readlines()

topPicks = []
numbering = []

for i in range(1, len(data), 10):
    topPicks.append(int((data[i].rstrip())[13:-1]))
    line = data[i - 1].rstrip()
    line = line.split("-------------------------- Prediction for ")[1]
    line = line.split(".png ---------------------------")[0]
    line = line[2:]
    numbering.append(int(line))

sortedNumbering = numbering[:]
sortedNumbering.sort(key = int)

rearrangedTopPicks = []

for i in range(len(sortedNumbering)):
    j = sortedNumbering[i]
    k = numbering.index(j)
    rearrangedTopPicks.append(topPicks[k])
    

with open("parsedoutput.csv", "w") as f:
    for i in rearrangedTopPicks:
        f.write(str(i) + "\n")
