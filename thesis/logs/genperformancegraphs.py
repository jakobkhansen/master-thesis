# /usr/bin/python

import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pathlib

from pandas.core.frame import DataFrame

plt.gcf().subplots_adjust(left=0.15)

for file in os.scandir("results/"):
    ccdetectfile = file.name
    if not ccdetectfile.endswith(".ccdetect"):
        continue
    sacafile = ccdetectfile.split(".")[0] + ".saca"
    print(sacafile)
    iclonesfile = ccdetectfile.split(".")[0] + ".iclones"
    chart_name = ccdetectfile.split(".")[0].split("_")[0] + " " + ccdetectfile.split(".")[0].split("_")[1]

    try:
        saca = pd.read_csv(f"results/{sacafile}", header=None)
    except:
        print("SACA not foudn")
        saca = None
        pass

    try:
        ccdetect = pd.read_csv(f"results/{ccdetectfile}", header=None)
    except:
        ccdetect = None
        pass

    try:
        iclones = pd.read_csv(f"results/{iclonesfile}", header=None)
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
    print(df)
    ax = df.plot(kind="bar", rot=0, title=chart_name)
    ax.set(xlabel="Revision", ylabel="ms (log)", yscale="log")
    ax.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))


    pdfname = ccdetectfile.split(".")[0].split("_")[0] + "_" + ccdetectfile.split(".")[0].split("_")[1]
    plt.tight_layout()
    plt.savefig(f"../figures/performancegraphs/{pdfname}.pdf")
