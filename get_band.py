# coding:utf-8
import arcpy
from arcpy.sa import *
import os


def get_R(out_path):
    files = arcpy.ListRasters("*", "tif")  # 查找目录中的 tif 格式文件
    for i, file in enumerate(files):  # 遍历
        try:
            arcpy.MakeRasterLayer_management(file, "red", band_index="1")  # 提取 R 波段
            Raster("red").save(out_path + os.sep + file)
            print "{} / {}".format(i + 1, len(files))  # 完成提示
        except:
            print file + " has a bug."  # 筛选出错误文件


def get_NIR(out_path):
    files = arcpy.ListRasters("*", "tif")  # 查找目录中的 tif 格式文件
    for i, file in enumerate(files):  # 遍历
        try:
            arcpy.MakeRasterLayer_management(file, "nir", band_index="4")  # 提取 NIR 波段
            Raster("nir").save(out_path + os.sep + file)
            print "{} / {}".format(i + 1, len(files))  # 完成提示
        except:
            print file + " has a bug."  # 筛选出错误文件
            
            
if __name__ == "__main__":
    arcpy.CheckOutExtension("spatial")  # 检查工具箱

    in_path_data1 = r"E:\project\pixelDichotomyStrengthAnalysis\data\yearsDatas\1"  # 输入文件路径
    in_path_data2 = r"E:\project\pixelDichotomyStrengthAnalysis\data\yearsDatas\2"  # 输入文件路径
    in_path_data3 = r"E:\project\pixelDichotomyStrengthAnalysis\data\yearsDatas\3"  # 输入文件路径

    R_path = r"E:\project\pixelDichotomyStrengthAnalysis\data\yearsDatas\R"  # 输出文件路径
    NIR_path = r"E:\project\pixelDichotomyStrengthAnalysis\data\yearsDatas\NIR"  # 输出文件路径

    arcpy.env.workspace = in_path_data1  # 设置当前工作目录
    print "begin to get R band:"
    get_R(R_path)

    print "begin to get NIR band:"
    get_NIR(NIR_path)
