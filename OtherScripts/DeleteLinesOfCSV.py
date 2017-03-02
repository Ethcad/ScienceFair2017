
# Copyright (c) 2017, Brendon Matusch. All rights reserved.

import os

with open("lines.txt", "r") as f:
    lines = f.readlines()

with open("data.csv", "r") as csv:
    ls = csv.readlines()

for i in range(len(lines)):
    lines[i] = lines[i].rstrip()

for i in range(len(ls)):
    ls[i] = ls[i].rstrip()

out = []

for i in range(len(lines) - 1, -1, -1):
    out.append(ls[int(lines[i]) - 1])

out.reverse()

with open("datanew.csv", "w") as new:
    for i in out:
        new.write(i + "\n")
