import subprocess
from common import *

f_dem = "/Volumes/LACIE SHARE/fr_mask_dem.tif"
#az:    0 top of raster
#      90 from the east
#     180 from the south
#     270 from the west
#     deflt: 315 from the north west
#alt:
#     altitude of the light, in degrees. 90 if the light comes from above the DEM, 0 if it is raking light.
#
# we want from south east:
az = 135


#https://www.suncalc.org/#/40.9991,-121.2424,3/2018.11.22/21:32/1/0
az = 294.4
alt = -54

HSHADE = False
if HSHADE:
    if 0:
        subprocess.call(["gdaldem", "hillshade", r"/Volumes/LACIE SHARE/fr_mask_dem.tif", \
             r"/Volumes/LACIE SHARE/fr_mask_hillshade.tif", "-z", "1.0", "-s", "111120.0", \
             "-az", "135.0", "-alt", "45.0"])


    import gdal
    ds = gdal.Open("/Volumes/LACIE SHARE/fr_mask_hillshade.tif")
    hs = ds.GetRasterBand(1).ReadAsArray()
    #hs[hs < -99] = np.nan
    plt.imshow(hs, interpolation="none")
    plt.colorbar()
    plt.show()

EXHAUST = False
if EXHAUST:
    if 1:
        subprocess.call(["gdaldem", "hillshade", r"/Volumes/LACIE SHARE/fr_mask_dem.tif", \
                         r"/Volumes/LACIE SHARE/fr_mask_exhaust.tif", "-z", "1.0", "-s", "111120.0", \
                         "-az", "240.0", "-alt", "0.0"])

    import gdal

    ds = gdal.Open("/Volumes/LACIE SHARE/fr_mask_exhaust.tif")
    hs = ds.GetRasterBand(1).ReadAsArray()
    # hs[hs < -99] = np.nan
    plt.imshow(hs, interpolation="none")
    plt.colorbar()
    plt.show()

if 1:
    if 1:
        subprocess.call(["gdaldem", "hillshade", r"/Volumes/LACIE SHARE/fr_mask_dem.tif", \
                         r"/Volumes/LACIE SHARE/fr_mask_exhaust20.tif", "-z", "1.0", "-s", "111120.0", \
                         "-az", "240.0", "-alt", "20.0"])

    import gdal

    ds = gdal.Open("/Volumes/LACIE SHARE/fr_mask_exhaust20.tif")
    hs = ds.GetRasterBand(1).ReadAsArray()
    # hs[hs < -99] = np.nan
    plt.imshow(hs, interpolation="none")
    plt.colorbar()
    plt.show()
