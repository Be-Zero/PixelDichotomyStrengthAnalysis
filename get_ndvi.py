# coding:utf-8
import arcpy
from arcpy.sa import *
import os

arcpy.CheckOutExtension("spatial")  # 检查工具箱

in_path_R = r"E:\Sentinel-2\shaanxi2017\R"  # 输入文件路径
in_path_NIR = r"E:\Sentinel-2\shaanxi2017\NIR"  # 输入文件路径
out_ndvi_path = r"E:\Sentinel-2\shaanxi2017\NDVI"  # 输出文件路径
tmp_path = r"E:\TMP"

arcpy.env.workspace = in_path_R  # 设置当前工作目录
files = arcpy.ListRasters("*", "tif")  # 查找目录中的 tif 格式文件
arcpy.env.workspace = tmp_path  # 设置当前工作目录
for file in files:  # 遍历
    try:
        ndvi = (Raster(in_path_NIR + os.sep + file) - Raster(in_path_R + os.sep + file)) / (Raster(in_path_NIR + os.sep + file) + Raster(in_path_R + os.sep + file))  # 计算 ndvi 指数
        ndvi.save(out_ndvi_path + os.sep + file)  # 将 ndvi 指数存为 tif 格式
        print file + " is done!"  # 完成提示

    except:
        print file + " has a bug."  # 筛选出错误文件
