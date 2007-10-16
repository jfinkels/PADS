from PartialCube import *

duads = [(1<<i)+(1<<j) for i in range(6) for j in range(i)]

synthemes = dict([((1<<i)+(1<<j)+(1<<k),(i,j,k))
                  for i in range(15) for j in range(i) for k in range(j)
                  if duads[i] & duads[j] == duads[i] & duads[k]
                    == duads[j] & duads[k] == 0])

TutteCoxeterGraph = {}

for v in duads:
    TutteCoxeterGraph[-v] = []

for v in synthemes:
    i,j,k = synthemes[v]
    TutteCoxeterGraph[v] = [-duads[i],-duads[j],-duads[k]]
    TutteCoxeterGraph[-duads[i]].append(v)
    TutteCoxeterGraph[-duads[j]].append(v)
    TutteCoxeterGraph[-duads[k]].append(v)
