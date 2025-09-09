import os
# Path to PROJLIB for gdal
os.environ['PROJ_LIB'] = r'Path to PROJLIB for gdal'
import numpy as np
from pathlib import Path
from osgeo import gdal

path = os.path.dirname(os.path.abspath(__file__))
p = Path(path).glob('*.tif')
for i in p:
    src_ds = gdal.Open(str(i))
    prj = src_ds.GetProjection()
    tiff_column = src_ds.RasterXSize
    tiff_row = src_ds.RasterYSize
    gdal_data_type = gdal.GDT_UInt16
    geotif_driver_name = r'GTiff'
    geotransform = src_ds.GetGeoTransform()
    #no_data = src_ds.GetRasterBand(8).GetNoDataValue()
    no_data = 0
    four_band_array = src_ds.GetRasterBand(4).ReadAsArray()
    two_band_array = src_ds.GetRasterBand(2).ReadAsArray()
    three_band_array = src_ds.GetRasterBand(3).ReadAsArray()
    eight_band_array = src_ds.GetRasterBand(8).ReadAsArray()
    ten_band_array = src_ds.GetRasterBand(10).ReadAsArray()
    nine_band_array = src_ds.GetRasterBand(9).ReadAsArray()
    one_band_array = src_ds.GetRasterBand(1).ReadAsArray()
    new_array = np.empty_like(four_band_array)
    new_array[((ten_band_array > 850) & (one_band_array > 2000)) |
              ((three_band_array > 6000) & (eight_band_array > 4000))
    ] = 1
    percent = str(round(((np.count_nonzero(new_array)*100)/new_array.size),2))
    driver = gdal.GetDriverByName(geotif_driver_name)
    output_raster = driver.Create(str(Path(path,'masks',i.stem+"_mask_cloud="+percent+"%.tif")), tiff_column, tiff_row, 1, gdal_data_type)
    output_band = output_raster.GetRasterBand(1)
    output_band.SetNoDataValue(0)
    output_band.WriteArray(new_array,0,0)
    output_raster.SetGeoTransform(geotransform)
    output_raster.SetProjection(prj)