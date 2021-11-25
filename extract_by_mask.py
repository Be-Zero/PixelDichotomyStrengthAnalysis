import arcpy
from arcpy import env
from arcpy.sa import *
import os


arcpy.CheckOutExtension("Spatial")
in_path = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\Vegetation_coverage"
mask_data = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\national_borders\national_borders.shp"
out_path = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\extract_by_mask"
dirs = os.listdir(in_path)
flag = 0
for dir in dirs:
    env.workspace = in_path + os.sep + dir
    files = arcpy.ListRasters(raster_type='TIF')
    for file in files:
        out = ExtractByMask(file, mask_data)
        if os.path.exists(out_path + os.sep + file.split('.')[0]) == False:
            os.mkdir(out_path + os.sep + file.split('.')[0])
        out.save(out_path + os.sep + file.split('.')[0] + os.sep + file)
    flag+=1
    print flag
print "ok!"