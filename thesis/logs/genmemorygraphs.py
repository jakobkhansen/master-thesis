#! /usr/bin/python
import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pathlib

from pandas.core.frame import DataFrame



results = {}
codebases = []
for line in open("memory.txt"):
    if (line.strip() == ""):
        continue
    linesplit = line.strip().split(" ")
    codebase = linesplit[0]
    tool = " ".join(linesplit[1:len(linesplit) - 1])
    memoryusage = int(linesplit[len(linesplit) - 1])

    if codebase not in codebases:
        codebases.append(codebase)

    if tool not in results:
        results[tool] = []
    results[tool].append(memoryusage)

    
results["iClones"].append(0)
df = DataFrame(results)
df = df[["CCDetect SACA", "CCDetect incremental", "iClones"]]
df = df.set_axis(codebases, axis=0)
ax = df.plot(kind="bar", rot=0, title="Memory usage")
ax.set(xlabel="Code base (increasing size)", ylabel="Peak memory usage (MB)")
plt.tight_layout()
plt.savefig(f"../figures/memoryusage.pdf")
