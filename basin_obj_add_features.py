from common import *
import gdal

basin_obj = cPickle.load(open("output/basin_obj.cPickle", "rb"))
#feature_names_test = ["conv-canopy", "hillshade"]
POPULATE_FEAT = True
if POPULATE_FEAT:
    #first time call this:
    #from basin_obj_loader import *
    #afterwards this (no need to repopulate)
    OVERWRITE = False

    for feature_n in feature_names_test:
        # TODO: to increase speed, load it once, and then call the functions
        if "conv" in feature_n:
            extra_arg = CONV
        else:
            extra_arg = None
        basin_obj.extract_features_from_tif_to_stations(feature_names_tif_path[feature_n], feature_n, OVERWRITE, extra_arg)

    cPickle.dump(basin_obj, open("output/basin_obj.cPickle", "wb"))

#check on features
print basin_obj.get_features_table(feature_names_test)