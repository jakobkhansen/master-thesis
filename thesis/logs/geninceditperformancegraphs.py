#! /usr/bin/python

import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pathlib

from pandas.core.frame import DataFrame

plt.gcf().subplots_adjust(left=0.15)

for file in os.scandir("incedit_results/"):
    ccdetectfile = file.name
    if not ccdetectfile.endswith(".ccdetect"):
        continue
    sacafile = ccdetectfile.split(".")[0] + ".saca"
    print(sacafile)
    iclonesfile = ccdetectfile.split(".")[0] + ".iclones"
    chart_name = ccdetectfile.split(".")[0].split("_")[0] + " " + ccdetectfile.split(".")[0].split("_")[1]

    try:
        saca = pd.read_csv(f"incedit_results/{sacafile}", header=None)
        if "INS" in sacafile:
            saca = saca[saca.columns[::-1]]
            last = saca.pop(saca.columns[-1])
            saca.insert(0, 0, last)
    except Exception as e:
        print("SACA not foudn")
        print(e)
        saca = None
        pass

    try:
        ccdetect = pd.read_csv(f"incedit_results/{ccdetectfile}", header=None)
        if "INS" in ccdetectfile:
            ccdetect = ccdetect[ccdetect.columns[::-1]]
            last = ccdetect.pop(ccdetect.columns[-1])
            ccdetect.insert(0, 0, last)
    except:
        ccdetect = None
        pass

    try:
        iclones = pd.read_csv(f"incedit_results/{iclonesfile}", header=None)
        if "INS" in iclones:
            iclones = iclones[iclones.columns[::-1]]
            last = iclones.pop(iclones.columns[-1])
            iclones.insert(0, 0, last)
    except:
        iclones = None
        pass



    df = pd.DataFrame({})
    if (isinstance(saca, DataFrame)):
        df["CCDetect SACA"] = list(saca.iloc[0])
    if (isinstance(ccdetect, DataFrame)):
        df["CCDetect incremental"] = list(ccdetect.iloc[0])
    if (isinstance(iclones, DataFrame)):
        df["iClones"] = list(iclones.iloc[0])
    columns = [0,1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
    df["changes"] = columns

    ax = df.plot(x="changes", kind="bar", rot=0, title=chart_name)
    xlabel = "Number of insertions" if "INS" in ccdetectfile else "Number of deletions"
    ax.set(xlabel=xlabel, ylabel="ms (log)", yscale="log")
    ax.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))


    pdfname = ccdetectfile.split(".")[0].split("_")[0] + "_" + ccdetectfile.split(".")[0].split("_")[1]
    plt.tight_layout()
    plt.savefig(f"../figures/incedit_performancegraphs/{pdfname}.pdf")
