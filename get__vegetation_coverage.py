# coding=utf-8

import os
import arcpy
from arcpy.sa import *
from get_confidence import get_confidence


arcpy.CheckOutExtension("spatial") # 检查外部扩展
arcpy.gp.overwriteOutput = 1 # 覆盖之前的文件

dirs = 'D:/Documentation/Project/Grassland ecology/Grassland_ecology/data/conversion/'
out_dir = 'D:/Documentation/Project/Grassland ecology/Grassland_ecology/data/Vegetation_coverage/'
asc_dir = 'D:/Documentation/Project/Grassland ecology/Grassland_ecology/data/gimms_ndvi_qd_1981-2002_exp/'
files = os.listdir(dirs)

for file in files:
    if os.path.exists(out_dir + file) == False:
        os.mkdir(out_dir + file)
    out_path = out_dir + file + os.sep
    dir = dirs + file + os.sep
    arcpy.env.workspace = dir
    rasters = arcpy.ListRasters(raster_type='TIF')

    for raster in rasters:
        inRaster = Raster(raster)
        Min, Max = get_confidence(asc_dir + file + ".asc")
        ans = Con(inRaster < Min, 0, Con((inRaster >= Min) & (inRaster <= Max), (inRaster - Min)/(Max - Min), 1))
        ans.save(out_path + file + ".tif")
        print file + " is done!"

print "OK!"