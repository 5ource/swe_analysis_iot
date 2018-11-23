from common import *
from confidential import *

#use meter
#use UTC
#load data
#exit(0)

#first time call this
from basin_obj_loader import *


bkl.add_stations_in_extent(basin_obj.stations)

grz.add_stations_in_extent(basin_obj.stations)

ktl.add_stations_in_extent(basin_obj.stations)

#plot all stations individually
if 0:
    bkl.show_stations_data_all(wys)
    ktl.show_stations_data_all(wys)
    grz.show_stations_data_all(wys)

outdir = "output/plot_pillow_vs_WSNs/"

#plot 1
PLOT_PILLOW_WSN_COURSES = 0
if PLOT_PILLOW_WSN_COURSES :
    for wy in [2017, 2018]:
        if wy == 2018:
            bkl.plot_pillow_vs_WSNs(wy, xclude_ids = ["Bklws0"])
        else:
            bkl.plot_pillow_vs_WSNs(wy)
        grz.plot_pillow_vs_WSNs(wy)
        ktl.plot_pillow_vs_WSNs(wy)
    multipage(outdir + "pillows_wsn_courses.pdf")
    #plt.show()

#plot 2 - inter-year variability
if 0:
    for wy in [2017, 2018]:
        if wy == 2018:
            bkl.plot_normalized_delta_from_pillow(wy, xclude_ids = ["Bklws0"])
        else:
            bkl.plot_normalized_delta_from_pillow(wy)
        grz.plot_normalized_delta_from_pillow(wy)
        ktl.plot_normalized_delta_from_pillow(wy)
    plt.show()

if 0:
    bkl.get_normalized_mean_delta_from_pillow(wys)
    grz.get_normalized_mean_delta_from_pillow(wys)
    ktl.get_normalized_mean_delta_from_pillow(wys)
    plt.show()

'''
    used in paper for intra-1km2 inter-year spatial stationarity
    returns pandas table node_id / %devWY1, %devWY2 ....
'''
if 1:
    bkl_df = bkl.get_normalized_temp_mean_dev_from_wsn_mean(wys, pct_bad=50)
    grz_df = grz.get_normalized_temp_mean_dev_from_wsn_mean(wys, pct_bad=50)
    ktl_df = ktl.get_normalized_temp_mean_dev_from_wsn_mean(wys, pct_bad=50)
    bkl_df.to_csv(outdir + "bkl_intra_dev.csv")
    grz_df.to_csv(outdir + "grz_intra_dev.csv")
    ktl_df.to_csv(outdir + "ktl_intra_dev.csv")

'''
    used in paper for intra-1km2 inter-year spatial stationarity
    returns pandas table node_id / rankWY1, rankWY2, deltaRank
'''
if 1:
    bkl_df = bkl.get_rank_temp_mean(wys, pct_bad=50)
    grz_df = grz.get_rank_temp_mean(wys, pct_bad=50)
    ktl_df =  ktl.get_rank_temp_mean(wys, pct_bad=50)
    bkl_df.to_csv(outdir + "bkl_intra_rank.csv")
    grz_df.to_csv(outdir + "grz_intra_rank.csv")
    ktl_df.to_csv(outdir + "ktl_intra_rank.csv")
'''
    used in paper for inter-1km2-site inter-year spatial stationarity
    returns pandas table node_id / rankWY1, rankWY2, deltaRank   and  node_id / %devWY1, %devWY2 ....
'''
if 1:
    inter_sites_df = bkl.get_rank_temp_mean_site_aggregated(wys, [grz, ktl])
    inter_sites_df.to_csv(outdir + "bkl_ktl_grz_inter_dv_rank.csv")