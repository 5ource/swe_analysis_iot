import cPickle
from common import *
import sys
sys.path.append('../sno/')
from objects import station, geo_extent, STATION_TYPES
from confidential import *
from matplotlib import pyplot as plt

#use meter
#use UTC

#load data
basin_obj = cPickle.load(open("../sno/scripts/cdec/output/Feather.cPickle", "rb"))
wsn_stations_objs = cPickle.load(open("../sno/scripts/wsn/output/wsn_stations.cPickle", "rb"))
basin_obj.convert_to_meters()
for k in wsn_stations_objs:
    wsn_stations_objs[k].force_active_by_wys()
    wsn_stations_objs[k].convert_to_meters()    #already in meters
#consolidate
basin_obj.add_stations(wsn_stations_objs)
#basin_obj.show_stations_data_all(wys)
print basin_obj.stations.keys()
#exit(0)


bkl = geo_extent("BKL", "BKL_1km2", extent_ul_lr_latlon=bkl_xtent)
bkl.add_stations_in_extent(basin_obj.stations)
grz = geo_extent("GRZ", "GRZ_1km2", extent_ul_lr_latlon=grz_xtent)
grz.add_stations_in_extent(basin_obj.stations)
ktl = geo_extent("KTL", "KTL_1km2", extent_ul_lr_latlon=ktl_xtent)
ktl.add_stations_in_extent(basin_obj.stations)

#plot all stations individually
if 0:
    bkl.show_stations_data_all(wys)
    ktl.show_stations_data_all(wys)
    grz.show_stations_data_all(wys)


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

    plt.show()

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
if 0:
    print bkl.get_normalized_temp_mean_dev_from_wsn_mean(wys, pct_bad=50)
    print grz.get_normalized_temp_mean_dev_from_wsn_mean(wys, pct_bad=50)
    print ktl.get_normalized_temp_mean_dev_from_wsn_mean(wys, pct_bad=50)

'''
    used in paper for intra-1km2 inter-year spatial stationarity
    returns pandas table node_id / rankWY1, rankWY2, deltaRank
'''
if 0:
    print bkl.get_rank_temp_mean(wys, pct_bad=50)
    print grz.get_rank_temp_mean(wys, pct_bad=50)
    print ktl.get_rank_temp_mean(wys, pct_bad=50)

'''
    used in paper for inter-1km2-site inter-year spatial stationarity
    returns pandas table node_id / rankWY1, rankWY2, deltaRank   and  node_id / %devWY1, %devWY2 ....
'''
if 1:
    print bkl.get_rank_temp_mean_site_aggregated(wys, [grz, ktl])