import arcpy
from arcpy import env
from arcpy.sa import *
import os


in_path = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\extract_by_mask"
out_path = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\years_data"
years_path = os.listdir(in_path)
for years in years_path:
    arr = []
    dirs = os.listdir(in_path + os.sep + years)
    for dir in dirs:
        env.workspace = in_path + os.sep + years + os.sep + dir
        files = arcpy.ListRasters(raster_type='TIF')
        for file in files:
            arr.append(in_path + os.sep + years + os.sep + dir + os.sep + file)

    arcpy.CheckOutExtension("Spatial")
    out = CellStatistics(arr, "MEAN")
    if os.path.exists(out_path + os.sep+ years) == False:
        os.mkdir(out_path + os.sep+ years)
    out.save(out_path + os.sep+ years + os.sep + years + '.tif')
print "ok!"