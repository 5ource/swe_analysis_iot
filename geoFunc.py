from FVarDefs import    *
from FuncDefs import    *
from LocDefs import     *

from math import sin, cos, sqrt, atan2, radians

#raster utils

km2_extent = [
    #bucks
    (39.858428, -121.256183), (39.851730, -121.247301)
]

points_latlon = [
    [39.85344,	-121.25085],
    [39.85238,	-121.2536],
    [39.85291,	-121.25288],
    [39.85356944,	-121.24912],
    [39.85527,	-121.25411],
    [39.8548,	-121.2533],
    [39.85743,	-121.25127],
    [39.85653,	-121.24835],
    [39.85684,	-121.25103],
    [39.85555,	-121.24849],
    [39.85413,	-121.25051],
    [39.85459,	-121.25109],
]

ELEVATION = 0
VEGETATION = 0

#all good

loc = "/Volumes/Untitled/malek18WSNs Data/"
loc = "/Volumes/LACIE SHARE/"

'''
returns boolean if latlon inside bounding box extent
extent should be ul, lr latlons
'''
def in_extent(latlon, extent):
     return latlon[0] < extent[0][0] and latlon[0] > extent[1][0] \
            and abs(latlon[1]) < abs(extent[0][1]) and abs(latlon[1]) > abs(extent[1][1])

'''
overlays points on raster image given latlon
TODO: add labels
'''
def overlay_fig_latlons(ds_or_fpath, latlons):
    rcs = latlons_to_rcs(latlons, ds_or_fpath)
    rcs = np.array(rcs)
    plt.scatter(rcs[:,1], rcs[:,0])

'''
converts ds_or_fpath to ds
'''
def get_ds(ds_or_fpath, arg=None):
    # assume it is fpath
    try:
        assert isinstance(ds_or_fpath, str)
        ds_or_fpath = gdal.Open(ds_or_fpath, arg)
    except:
        #it is ds, nothing to do
        pass
    return ds_or_fpath

'''
converts ds_or_fpath to ds readonly
'''
def reado_ds(ds_or_fpath):
    return get_ds(ds_or_fpath, arg=gdal.GA_ReadOnly)

'''
returns list of raster values extracted at rcs
'''
def extract_rasterValues_at_rcs(ds_or_fpath, rcs):
    ds = reado_ds(ds_or_fpath)
    arr = ds.GetRasterBand(1).ReadAsArray()
    rcs = np.array(rcs)
    return arr[rcs[:,0], rcs[:,1]]

'''
returns list of raster values extracted at latlons
ds_or_fpath can be either ds or fpath
'''
def extract_rasterValues_at_latlons(ds_or_fpath, latlons):
    rcs = latlons_to_rcs(latlons, ds_or_fpath)
    print "rcs = ", rcs
    return extract_rasterValues_at_rcs(ds_or_fpath, rcs)

'''
Returns None: clips raster ds/fpath by bounding box: xtent, and saves to clipped_fpath
'''
def clip_extent_from_raster_toFile(xtent, clipped_fpath, ds_or_fpath):
    # projwin must be in format: ulx uly lrx lry:
    projwin = get_gdal_projwin_from_extent(xtent)
    clip = gdal.Translate(clipped_fpath, ds_or_fpath, projWin=projwin)  # [-75.3, 5.5, -73.5, 3.7])
    clip = None

'''
Returns gdal projwin [ulx uly lrx lry]:
'''
def get_gdal_projwin_from_extent(xtent):
    return [xtent[0][1], xtent[0][0], xtent[1][1], xtent[1][0]]

'''
returns km2 area of extent
'''
def area_from_extent(latlonUL_latlonLR): #, fpath=None, ds=None, mem=False):
    ul = latlonUL_latlonLR[0]
    lr = latlonUL_latlonLR[1]
    ur = (ul[0], lr[1])
    ll = (lr[0], ul[1])
    horiz_dist = meter_distance_from_lat_lon(ul, ur)/1000.0
    vert_dist  = meter_distance_from_lat_lon(ur, lr)/1000.0
    return vert_dist * horiz_dist
'''
Takes latlons list of latitude, longitude pairs, and 
Returns their row/columns
'''
def latlons_to_rcs(latlons, ds_or_fpath):
    #assume it is ds
    ds = get_ds(ds_or_fpath, gdal.GA_ReadOnly)
    transform = ds.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = -transform[5]
    rcs = []
    for latlon in latlons:
        col = int((latlon[1] - xOrigin) / pixelWidth)
        row = int((yOrigin - latlon[0]) / pixelHeight)
        rcs.append([row, col])
    return rcs

'''
Returns [upper left lon_lat, lower right lon_lat] of tiff map
'''
def get_ds_extent(fpath=None, ds=None, mem=False):
    if not mem:
        ds = gdal.Open(fpath, gdal.GA_ReadOnly)
    ulx, xres, xskew, uly, yskew, yres = ds.GetGeoTransform()
    lrx = ulx + (ds.RasterXSize * xres)
    lry = uly + (ds.RasterYSize * yres)
    return [(uly, ulx), (lry, lrx)]

'''
Takes 2 points locations as lat_lon
Returns the meter distance between those 2 points
'''
def meter_distance_from_lat_lon(lat_lon1, lat_lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat_lon1[0]) #52.2296756)
    lon1 = radians(lat_lon1[1]) #21.0122287)
    lat2 = radians(lat_lon2[0]) #52.406374)
    lon2 = radians(lat_lon2[1]) #16.9251681)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    print "d from ", lat_lon1, "to", lat_lon2, " = ", distance
    return distance * 1000
    #print("Result:", distance)
    #print("Should be:", 278.546, "km")

'''
Takes location of point latlon
Returns the pixel size at that location in meter as (pixel_size_lat, pixel_size_lon)
'''
def get_pixel_size_at_latlon(latlon, fpath=None, ds=None, mem=False):
    if not mem:
        ds = gdal.Open(fpath, gdal.GA_ReadOnly)
    transform = ds.GetGeoTransform()
    pixelWidth = transform[1]
    pixelHeight = -transform[5]
    next_pixel_right = (latlon[0], latlon[1]+pixelWidth)
    next_pixel_up    = (latlon[0] + pixelHeight, latlon[1])
    pixel_size_lat   = meter_distance_from_lat_lon(latlon, next_pixel_up) #not changing
    pixel_size_lon   = meter_distance_from_lat_lon(latlon, next_pixel_right)
    return (pixel_size_lat, pixel_size_lon)

'''
Returns pixel size in (deltaLon, deltaLat)
'''
def get_pixel_size(fpath):
    raster = gdal.Open(fpath, gdal.GA_ReadOnly)
    gt = raster.GetGeoTransform()
    print "geo transform = ", gt
    srs = osr.SpatialReference()
    srs.SetProjection(raster.GetProjection())
    print "LinearUnitsName, Units = ", srs.GetLinearUnitsName(), srs.GetLinearUnits()
    #print gt
    #(258012.37107330866, 2.11668210080698, 0.0, 163176.6385398821, 0.0, -2.1168501270110074)
    pixelSizeX = gt[1]
    pixelSizeY = -gt[5]
    #print pixelSizeX
    #2.11668210080698
    #print pixelSizeY
    #2.1168501270110074
    return (pixelSizeX, pixelSizeY)

def gdal_show(fname, show=True):
    ds = gdal.Open(fname, gdal.GA_ReadOnly)
    ar = ds.GetRasterBand(1).ReadAsArray()
    ar = ar.astype(float)
    #ar = float(ar)
    #print np.count_nonzero(np.isfinite(ar))
    #df = pd.DataFrame(ar)
    #print df.isnull().values.sum()
    #df.dropna()
    #ar = np.array(df, type=float)
    #plt.imshow(np.isnan(ar))
    #plt.colorbar()
    #plt.show()
    #exit(0)
    ar[ar >= 9999.9] = np.nan
    ar[ar <= -9999.0] = np.nan
    plt.figure()
    plt.imshow(ar, interpolation="none", cmap="terrain")
    plt.title(fname)
    plt.colorbar()
    if show:
        plt.show()

if 0:   #90m resolution
    gdal_show(loc +"fr_mask_dem_resampled.tif")
    gdal_show(loc +"feather asp 100m.tif")
    gdal_show(loc +"feather slope 100m.tif")
    gdal_show(loc +"feather veg 100m.tif")

if 1:   #3m resolution
    #gdal_show("fr_mask_dem.tif")
    #gdal_show("fr_mask_slope.tif")
    fname = "fr_mask_veg.tif"
    print "pixel size = ", get_pixel_size(loc + fname)
    latlonul_latlonlr = get_ds_extent(loc + fname)
    print "ds extent  = ", latlonul_latlonlr
    pSize_ul_m = get_pixel_size_at_latlon(latlonul_latlonlr[0], fpath=loc + fname)
    pSize_lr_m = get_pixel_size_at_latlon(latlonul_latlonlr[1], fpath=loc + fname)
    print "pixel size ul (m) = ", pSize_ul_m
    print "pixel size lr (m) = ", pSize_lr_m
    print "extent lat (km) = ", meter_distance_from_lat_lon(latlonul_latlonlr[0], latlonul_latlonlr[1])/1000.0
    feather_area = area_from_extent(latlonul_latlonlr)
    print "area of feather river = ", feather_area
    xtent_area   = area_from_extent(km2_extent)
    print "area of 1km2 = ", xtent_area
    #clip to extent
    #ds = gdal.Open(loc + "fr_mask_dem.tif")
    #ds = gdal.Open(loc + "fr_mask_veg.tif")
    #ds = gdal.Open(loc + "fr_mask_aspect.tif")
        #ds = gdal.Open(loc + "fr_mask_slope.tif")
    #projwin ulx uly lrx lry:
        #projwin = get_gdal_projwin_from_extent(km2_extent)
    #rast = ds.GetRasterBand(1).ReadAsArray()
    #ulY = km2_extent[0][0]
    #ulX = km2_extent[0][1]
    #lrY = km2_extent[1][0]
    #lrX = km2_extent[1][1]
    #clip = rast[ulY:lrY, ulX:lrX]
    #print clip
        #ds = gdal.Open(loc + "fr_mask_slope.tif")
    #print "projwin = ", projwin
        #clip = gdal.Translate(loc +'new.tif', ds, projWin=projwin)#[-75.3, 5.5, -73.5, 3.7])
        #clip = None
        #gdal_show(loc + 'new.tif')
    TEST_CLIPPING = False
    if TEST_CLIPPING:
        fname = "fr_mask_veg"
        #clip veg
        dst_fpath = loc + fname + "_clipped.tif"
        clip_extent_from_raster_toFile(km2_extent, dst_fpath, loc + fname + ".tif")
        gdal_show(dst_fpath, False)
        #convolution
        CONVOLVE = False
        if CONVOLVE:
            x = np.array([[0.1, 0.1, 1.0], [0.1, -4.3, 1.0], [1.0, 1.0, 1.0]])
            x/= np.sum(x)
            print x
            ds = gdal.Open(dst_fpath)
            veg = ds.GetRasterBand(1).ReadAsArray()
            conv_veg = scipy.signal.convolve2d(x, veg)
            plt.figure()
            plt.imshow(conv_veg, interpolation="none", cmap="terrain")
            plt.clim(0, 100)
            plt.colorbar()
            plt.show()

        #clip dem
        fname = "fr_mask_dem"

        dst_fpath = loc + fname + "_clipped.tif"
        clip_extent_from_raster_toFile(km2_extent, dst_fpath, loc + fname + ".tif")
        gdal_show(dst_fpath)

        fname = "fr_mask_aspect"
        #clip aspect
        dst_fpath = loc + fname + "_clipped.tif"
        clip_extent_from_raster_toFile(km2_extent, dst_fpath, loc + fname + ".tif")
        gdal_show(dst_fpath)

        fname = "fr_mask_slope"
        #clip slope
        dst_fpath = loc + fname + "_clipped.tif"
        clip_extent_from_raster_toFile(km2_extent, dst_fpath, loc + fname + ".tif")
        gdal_show(dst_fpath)
        #gdal_show("fr_mask_aspect.tif")

    # clip dem
    fname = "fr_mask_dem"
    dst_fpath = loc + fname + "_clipped.tif"
    fpath = loc + fname + ".tif"
    clip_extent_from_raster_toFile(km2_extent, dst_fpath, fpath)
    #gdal_show(dst_fpath)
    print "global values = ", extract_rasterValues_at_latlons(fpath, points_latlon)
    print "local  values = ", extract_rasterValues_at_latlons(dst_fpath, points_latlon)

    gdal_show(dst_fpath, show=False)
    overlay_fig_latlons(dst_fpath, points_latlon)

    gdal_show(fpath, show=False)
    overlay_fig_latlons(fpath, points_latlon)
    plt.show()

