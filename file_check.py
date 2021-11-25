# coding=utf-8
import os


# check if the file exists
f = open(r'D:\Documentation\Project\Grassland ecology\data\MODIS NDVI\download.txt')
dir = r'D:\Documentation\Project\Grassland ecology\data\MODIS NDVI\hdf'
path = r'D:\Documentation\Project\Grassland ecology\data\MODIS NDVI\check.txt'
line = f.readline()
save = open(path, mode='w')
count = 0
while line:
    if os.path.exists(dir + os.sep + line.split('/')[-1].replace('\n', '')) == False: # txt file has line breaks, we should ignore it
        save.writelines(line)
    count+=1
    print count
    line = f.readline()

print 'ok!'