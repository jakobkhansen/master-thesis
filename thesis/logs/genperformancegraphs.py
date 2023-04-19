# /usr/bin/python

import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pathlib

from pandas.core.frame import DataFrame

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

    pdfname = ccdetectfile.split(".")[0].split("_")[0] + "_" + ccdetectfile.split(".")[0].split("_")[1]
    plt.savefig(f"../figures/performancegraphs/{pdfname}.pdf")

#     x = np.array(range(3, 9))
#     y_nosig = np.array([800.450, 1200.648, 1601.243, 2001.556, 2401.533, 2804.002])
#
#     y_sig = np.array([811.426, 1222.255, 1619.571, 2040.650, 2453.965, 2858.508])
#
# # fz = 15
#     nosig_colour = "green"
#     sig_colour = "darkblue"
# # font = {"family": "", "weight": "bold", "size": 22}
# # mpl.rc("font", **font)
#     mpl.rcParams.update({"font.size": 13})
#
#     plt.plot(x, y_nosig, c=nosig_colour, label="Without signatures")
#     plt.scatter(x, y_nosig, c=nosig_colour)
#     plt.plot(x, y_sig, c=sig_colour, label="With signatures")
#     plt.scatter(x, y_sig, c=sig_colour)
#     plt.xlabel("Number of hosts in linear topology")
#     plt.ylabel("RTT (ms)")
#     plt.grid()
#     plt.legend()
#
#     pp = PdfPages("rtt_plot.pdf")
#     pp.savefig()
#     pp.close()
