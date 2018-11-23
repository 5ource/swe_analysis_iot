from common import *

#TODO:
# Run "basin_obj_add_features.py" to add features to the initially loaded "basin_obj_loader.py"

basin_obj = cPickle.load(open("output/basin_obj.cPickle", "rb"))
#wsn_stations_objs = cPickle.load(open("../sno/scripts/wsn/output/wsn_stations.cPickle", "rb"))
#basin_obj.convert_to_meters()
#for k in wsn_stations_objs:
#    wsn_stations_objs[k].force_active_by_wys()
#    wsn_stations_objs[k].convert_to_meters()    #already in meters
#consolidate
#basin_obj.add_stations(wsn_stations_objs)
#basin_obj.show_stations_data_all(wys)
#print basin_obj.stations.keys()

#station_types = [STATION_TYPES["WSN"], STATION_TYPES["Pillow"]]
#station_types = [STATION_TYPES["Pillow"]]
station_types = [STATION_TYPES["WSN"]]
extents = [bkl, grz, ktl]

outDir = "output/explained_variance_of_features/"
create_dir(outDir)

#compare canopy, canopy-conv
if 0:
    feature_names_can = ["canopy", "conv-canopy"]
    print basin_obj.get_features_table(feature_names_can)
    for extent in extents:
        for wy in wys:
            r2_by_feat, mean_swe, el_r2 = basin_obj.get_explained_variances_R2(wy, feature_names_can,
                                                       FEATURE_NAME_RANGE,
                                                       min_pct_of_sensors=50,
                                                       station_types=station_types,
                                                       inside_extent = extent)
            plt.figure()
            plt.title(extent.name +" wy = "+ str(wy))
            daxis = get_date_axis(wy)
            for fn in feature_names_can:
                plt.plot(daxis, r2_by_feat[fn], label=fn)
            plt.plot(get_date_axis(wy), el_r2, label="total")
            plt.plot(get_date_axis(wy), mean_swe/np.nanmax(mean_swe), label="mean_swe")
            plt.legend()
            #plt.show()
    multipage(outDir + "local_wsn_canopy_vs_conv-canopy.pdf")
    plt.close()

#all features
if 1:
    feature_names_all = feature_names_test
    x = ["elevation",
                      "aspect",
                      "slope",
                      "lat",
                      "lon",
                      "PRISM_ppt_normal",
                      "MargMonthMean"]
    for extent in extents:
        for wy in wys:
            r2_by_feat, mean_swe, el_r2, betas = basin_obj.get_explained_variances_R2(wy, feature_names_all,
                                                       FEATURE_NAME_RANGE,
                                                       min_pct_of_sensors=50,
                                                       station_types=station_types,
                                                       inside_extent = extent)
            #r2_by_feat = betas
            plt.figure()
            plt.title(extent.name +" wy = "+ str(wy))
            for fn in feature_names_all:
                plt.plot(get_date_axis(wy),r2_by_feat[fn], label=fn)
            plt.plot(get_date_axis(wy), el_r2, label="total")
            plt.plot(get_date_axis(wy), mean_swe/np.nanmax(mean_swe), label="mean_swe")
            plt.legend()
            #plt.show()
    multipage(outDir + "local_wsn_all_feat.pdf")

if 0:
    #global WSN
    feature_names_all = feature_names_test
    for wy in wys:
        r2_by_feat, mean_swe, el_r2 = basin_obj.get_explained_variances_R2(wy, feature_names_all,
                                                                    FEATURE_NAME_RANGE,
                                                                    min_pct_of_sensors=50,
                                                                    station_types=station_types,
                                                                    inside_extent=None) #extent)
        plt.figure()
        plt.title(extent.name + " wy = " + str(wy))
        for fn in feature_names_all:
            plt.plot(get_date_axis(wy), r2_by_feat[fn], label=fn)
        plt.plot(get_date_axis(wy), el_r2, label="total")
        plt.plot(get_date_axis(wy), mean_swe / np.nanmax(mean_swe), label="mean_swe")
        plt.legend()
        # plt.show()
    multipage(outDir + "global_wsn_all_feat.pdf")


if 1:
    #pillows only
    station_types = [STATION_TYPES["Pillow"]]
    feature_names_all = feature_names_test
    print basin_obj.get_features_table(feature_names_all)
    for wy in wys:
        r2_by_feat, mean_swe, el_r2, betas = basin_obj.get_explained_variances_R2(wy, feature_names_all,
                                                                    FEATURE_NAME_RANGE,
                                                                    min_pct_of_sensors=50,
                                                                    station_types=station_types,
                                                                    inside_extent=None) #extent)
        print "r2_by_feat = ", r2_by_feat.keys()
        #r2_by_feat = betas
        plt.figure()
        plt.title(" wy = " + str(wy))
        for fn in feature_names_all:
            plt.plot(get_date_axis(wy), r2_by_feat[fn], label=fn)
            #print "exception at fn = ", fn
            #print " r2_by_feat[fn] = ",  r2_by_feat[fn]
            #pass
        plt.plot(get_date_axis(wy), el_r2, label="total")
        plt.plot(get_date_axis(wy), mean_swe / np.nanmax(mean_swe), label="mean_swe")
        plt.legend()
        # plt.show()
    multipage(outDir + "global_pillows_only_all_feat.pdf")

if 0:
    # global all
    station_types = [STATION_TYPES["Pillow"], STATION_TYPES["WSN"]]
    feature_names_all = feature_names_test
    for wy in wys:
        r2_by_feat, mean_swe, el_r2 = basin_obj.get_explained_variances_R2(wy, feature_names_all,
                                                                    FEATURE_NAME_RANGE,
                                                                    min_pct_of_sensors=50,
                                                                    station_types=station_types,
                                                                    inside_extent=None)  # extent)
        plt.figure()
        plt.title("wy = " + str(wy))
        for fn in feature_names_all:
            plt.plot(get_date_axis(wy), r2_by_feat[fn], label=fn)
            #print "exception at fn = ", fn
            #print " r2_by_feat[fn] = ",  r2_by_feat[fn]
        plt.plot(get_date_axis(wy), el_r2, label="total")
        plt.plot(get_date_axis(wy), mean_swe / np.nanmax(mean_swe), label="mean_swe")
        plt.legend()
        # plt.show()
    multipage(outDir + "global_all_all_feat.pdf")