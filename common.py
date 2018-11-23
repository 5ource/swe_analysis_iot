wys = [2017, 2018]
from confidential import *
import sys
#needed for the objects library
sys.path.append('../sno/')
from objects import station, geo_extent, STATION_TYPES
from geoFunc import get_date_axis

#needed to load objects
import cPickle

from matplotlib import pyplot as plt

bkl = geo_extent("BKL", "BKL_1km2", extent_ul_lr_latlon=bkl_xtent)
grz = geo_extent("GRZ", "GRZ_1km2", extent_ul_lr_latlon=grz_xtent)
ktl = geo_extent("KTL", "KTL_1km2", extent_ul_lr_latlon=ktl_xtent)

loc = "/Volumes/LACIE SHARE/"

feature_names_tif_path = {
    "elevation"     :   loc + "fr_mask_dem.tif",
    "canopy"        :   loc + "fr_mask_veg.tif",
    "PRISM_ppt_normal":  loc + "PRISM_ppt_30yr_normal_800mM2_annual.tif",
    "aspect"        :   loc + "fr_mask_aspect.tif",
    "slope"         :   loc + "fr_mask_slope.tif",
    "conv-canopy"   :   loc + "fr_mask_veg.tif",    #computing conv aborted, taking too long
    "hillshade"     :   loc + "fr_mask_hillshade.tif",
    "ex"            :   loc + "fr_mask_exhaust.tif",
    "ex20"          :   loc + "fr_mask_exhaust20.tif",
    "lat"           :   None,
    "lon"           :   None,
    "MODIS"         :   None,
    "MargMonthMean" :   loc + "marg_monthly_mean/marg_mean_month_",
    "TRI"           :   loc + "fr_mask_TRI.tif",

}

FEATURE_NAME_RANGE = {
    "elevation"     :   [0, 5000],
    "canopy"        :   [0, 100],
    "PRISM_ppt_normal": [0, 10000],
    "aspect"        :   [-1000, 1000], #None, #TODO
    "slope"         :   [-1000, 1000], #None, #TODO
    "conv-canopy"   :   [-100, 100],
    "hillshade"     :   [0, 1000],
    "ex"            :   [0, 1000],
    "ex20"          :   [0, 1000],
    "lat"           :   [-1000, 1000],
    "lon"           :   [-1000, 1000],
    "MODIS"         :   None, #TODO
    "MargMonthMean" :   [0, 1000],
    "TRI"           :   [0, 1000]
}
feature_names = feature_names_tif_path.keys()


feature_names_test =  ["elevation",
                      "canopy",
                      "aspect",
                      "slope",
                      "lat",
                      "lon",
                      "conv-canopy",
                      "PRISM_ppt_normal",
                      "MargMonthMean",
                      "hillshade",
                       "ex",
                       "ex20",
                       "TRI"]


import numpy as np
CONV = np.array([[0.1, 0.1, 1.0], [0.1, -4.3, 1.0], [1.0, 1.0, 1.0]])
#CONV = np.array([[1.0, 1.0, 1.0], [1.0, -9.0, 1.0], [1.0, 1.0, 1.0]])
#CONV = np.array([[0.1, 0.1, 1.0], [0.1, -5.3, 1.0], [1.0, 1.0, 1.0]])
#CONV = np.array([[-1.0, -1.0, 2.0], [-1.0,   -1.0,  2.0], [-1.0, -1.0, 2.0]])
#CONV = CONV/np.sum(abs(CONV))
#print CONV

#for accumulation

#CONV = np.array([[-1.0, -1.0, -1.0], [-1.0, 8.0, -1.0], [-1.0, -1.0, -1.0]])
#CONV /= np.sum(abs(CONV))
#CONV = CONV[0]
#CONV /= np.sum(CONV)


from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

def multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)
    if figs is None:
        figs = [plt.figure(n) for n in plt.get_fignums()]
    for fig in figs:
        fig.savefig(pp, format='pdf', dpi=dpi)
    pp.close()
    plt.close('all')

def create_dir(outdir):
    import os
    if not os.path.exists(outdir):
        os.makedirs(outdir)