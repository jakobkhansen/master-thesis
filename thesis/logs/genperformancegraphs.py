# /usr/bin/python

import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

for file in os.scandir("performance/"):
    ccdetectfile = file.name
    if not ccdetectfile.endswith(".ccdetect"):
        continue
    iclonesfile = ccdetectfile.split(".")[0] + ".iclones"
    chart_name = ccdetectfile.split(".")[0].split("_")[0] + " " + ccdetectfile.split(".")[0].split("_")[1]
    print(iclonesfile)
    ccdetect = pd.read_csv(f"performance/{ccdetectfile}", header=None)
    iclones = pd.read_csv(f"performance/{iclonesfile}", header=None)
    df = pd.DataFrame({"CCDetect": list(ccdetect.iloc[0]), "iClones": list(iclones.iloc[0])})
    print(df)
    ax = df.plot(kind="bar", rot=0, title=chart_name)
    ax.set(xlabel="Insertions", ylabel="ms (log)", yscale="log")

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
