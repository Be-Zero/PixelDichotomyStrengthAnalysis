import os
import shutil

if __name__ == '__main__':
    in_path = 'E:/project/pixelDichotomyStrengthAnalysis/data/1/Img/clip/'
    dirs = os.listdir(in_path)
    for i in dirs:
        files = os.listdir(in_path + i)
        for j in files:
            if not os.path.exists(in_path + j[:-4]):
                os.mkdir(in_path + j[:-4])
                os.mkdir(in_path + j[:-4] + '/Img')
            shutil.copyfile(in_path + i + '/' + j, in_path + j[:-4] + '/Img/' + i + '.tif')
    # in_path = 'E:/project/pixelDichotomyStrengthAnalysis/data/1/Img/clip/'
    # dirs = os.listdir(in_path)
    # for dir in dirs:
    #     files = os.listdir(in_path + dir)
    #     os.mkdir(in_path + dir + '/Img')
    #     for file in files:
    #         shutil.move(in_path + dir + '/' + file, in_path + dir + '/Img/' + file)