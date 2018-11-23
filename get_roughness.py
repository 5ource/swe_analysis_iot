import subprocess
from common import *

f_dem = "/Volumes/LACIE SHARE/fr_mask_dem.tif"

TRI = True
if TRI:
    if 0:
        subprocess.call(["gdaldem", "TRI", r"/Volumes/LACIE SHARE/fr_mask_dem.tif", \
             r"/Volumes/LACIE SHARE/fr_mask_tri.tif"])


    import gdal
    ds = gdal.Open("/Volumes/LACIE SHARE/fr_mask_tri.tif")
    hs = ds.GetRasterBand(1).ReadAsArray()
    hs[hs < -99] = np.nan
    plt.imshow(hs, interpolation="none")
    plt.colorbar()
    plt.show()
