from common import *

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