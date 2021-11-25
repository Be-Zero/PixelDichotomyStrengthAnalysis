# coding=utf-8
import numpy as np
import arcpy
from arcpy.sa import *


def load_img_to_array(img_file_path):
    inRas = arcpy.Raster(img_file_path)
    lowerLeft = arcpy.Point(inRas.extent.XMin, inRas.extent.YMin)
    ndarray = arcpy.RasterToNumPyArray(inRas)
    ndarray = ndarray.reshape(1, -1)
    ndarray.sort()
    ndarray = ndarray[ndarray>=-1] # 取正常的NDVI值
    q_5 = np.percentile(ndarray, 5)
    q_15 = np.percentile(ndarray, 15)
    q_30 = np.percentile(ndarray, 30)
    q_60 = np.percentile(ndarray, 60)

    return [[0, q_5, 0], [q_5, q_15, 1], [q_15, q_30, 2], [q_30, q_60, 3], [q_60, 1, 4]]

in_path1 = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\years_data\1980s\1980s.tif"
in_path2 = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\years_data\1990s\1990s.tif"
in_path3 = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\years_data\2000s\2000s.tif"

p1 = load_img_to_array(in_path1)
p2 = load_img_to_array(in_path2)
p3 = load_img_to_array(in_path3)

out_path1 = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\reclassify\1980s\1980s.tif"
out_path2 = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\reclassify\1990s\1990s.tif"
out_path3 = r"D:\Documentation\Project\Grassland ecology\Grassland_ecology\data\reclassify\2000s\2000s.tif"

out1 = Reclassify(in_path1, "Value", RemapRange(p1))
out2 = Reclassify(in_path2, "Value", RemapRange(p2))
out3 = Reclassify(in_path3, "Value", RemapRange(p3))

out1.save(out_path1)
out2.save(out_path2)
out3.save(out_path3)