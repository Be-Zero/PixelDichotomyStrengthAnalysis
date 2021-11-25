#encoding:utf-8
import os
import arcpy


dir = 'D:/Documentation/Project/Grassland ecology/Grassland_ecology/data/gimms_ndvi_qd_1981-2002_exp/'
files = os.listdir(dir)

for f in files:
    if os.path.splitext(f)[1] == '.asc':
        # Script arguments...
        input_raster_file = dir + f # 文件名
        # output_data_type = "DOUBLE" # 数据类型

        # Local variables...
        raster_format = "TIFF" # 文件类型
        output_workspace = 'D:/Documentation/Project/Grassland ecology/Grassland_ecology/data/conversion/' + os.path.splitext(f)[0] # 输出路径
        os.mkdir(output_workspace)

        # file name process
        output_raster = output_workspace + os.sep + os.path.splitext(f)[0] + ".tif" # 输出文件名

        if os.path.exists(output_raster) == False:
            # print input_raster_file

            # Process: Raster To Other Format (multiple)...
            arcpy.RasterToOtherFormat_conversion(input_raster_file, output_workspace, raster_format)
            # print output_raster
print "ALL DONE"
