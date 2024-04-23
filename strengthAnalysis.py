# coding=utf-8
import os
from copy import deepcopy

import numpy as np
from osgeo import gdal


class strengthAnalysis:
    # init
    def __init__(self, path, mode='main'):
        in_path = path + "Img/"
        reclass_path = path + "reclass/"
        change_path = path + 'change/'
        np_path = path + "numpy/"
        if os.path.exists(in_path) == False:
            os.mkdir(in_path)
        if os.path.exists(reclass_path) == False:
            os.mkdir(reclass_path)
        if os.path.exists(change_path) == False:
            os.mkdir(change_path)
        if os.path.exists(np_path) == False:
            os.mkdir(np_path)
        if mode == 'main':
            # 获取图像
            imgs, self.files = self.reclass(in_path, reclass_path)
            
            # 获取图像个数
            self.n = len(imgs)
            
            for i in range(self.n-1):
                self.files[i] = self.files[i][:-4] + '_' + self.files[i+1][:-4]
            self.files = self.files[:-1]
            # self.files = np.array(self.files[:-1])
            self.rate = self.writeChange(reclass_path, change_path)

            # 初始状态
            self.category = self.getInit(imgs, self.n)

            # 时间跨度
            self.var = self.getVar(imgs, self.n)
            del imgs

            self.increase = []
            self.decrease = []
            for v in self.var:
                self.increase.append([v[1][0] + v[2][0] + v[3][0] + v[4][0],
                                      v[0][1] + v[2][1] + v[3][1] + v[4][1],
                                      v[0][2] + v[1][2] + v[3][2] + v[4][2],
                                      v[0][3] + v[1][3] + v[2][3] + v[4][3],
                                      v[0][4] + v[1][4] + v[2][4] + v[3][4]])
                self.decrease.append([v[0][1] + v[0][2] + v[0][3] + v[0][4],
                                      v[1][0] + v[1][2] + v[1][3] + v[1][4],
                                      v[2][0] + v[2][1] + v[2][3] + v[2][4],
                                      v[3][0] + v[3][1] + v[3][2] + v[3][4],
                                      v[4][0] + v[4][1] + v[4][2] + v[4][3]])

            self.increase = np.array(self.increase, dtype='float')
            self.decrease = np.array(self.decrease, dtype='float')

            np.save(np_path + 'category.npy', self.category)
            np.save(np_path + 'var.npy', self.var)
            np.save(np_path + 'increase.npy', self.increase)
            np.save(np_path + 'decrease.npy', self.decrease)
            np.save(np_path + 'files.npy', self.files)
        else:
            self.category = np.load(np_path + 'category.npy')
            self.var = np.load(np_path + 'var.npy')
            self.increase = np.load(np_path + 'increase.npy')
            self.decrease = np.load(np_path + 'decrease.npy')
            self.files = np.load(np_path + 'files.npy')
            self.n = len(self.category)
            self.rate = self.writeChange(reclass_path, change_path)

    def file_filter(self, f):
        if f[-4:] == '.tif':
            return True
        else:
            return False

    def isRange(self, v, l, r):
        if l < v and v <= r:
            return True
        else:
            return False

    def write_img(self, filename, im_proj, im_geotrans, im_data):
        # 判断栅格数据的数据类型
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        # 判读数组维数
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape

        # 创建文件
        driver = gdal.GetDriverByName("GTiff")
        dataset = driver.Create(
            filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影

        if im_bands == 1:
            dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
        else:
            for i in range(im_bands):
                dataset.GetRasterBand(i+1).WriteArray(im_data[i])
        del dataset

    def get_vfd(self, data):
        pdata = deepcopy(data)
        pdata.sort()
        q_5 = np.percentile(pdata, 5)
        q_95 = np.percentile(pdata, 95)
        del pdata
        for i, v in enumerate(data):
            if q_95 - v != 0:
                data[i] = (v - q_5) / (q_95 - q_5)
            else:
                data[i] = 1
        return data

    def reclass(self, in_path, out_path):
        files = os.listdir(in_path)
        files = list(filter(self.file_filter, files))  # 筛选tif
        files.sort()
        imgs = []
        for file in files:
            img = gdal.Open(in_path + file)
            width = img.RasterXSize  # 栅格矩阵的列数
            height = img.RasterYSize  # 栅格矩阵的行数
            geotrans = img.GetGeoTransform()  # 仿射矩阵，左上角像素的大地坐标和像素分辨率
            proj = img.GetProjection()  # 地图投影信息，字符串表示
            data = img.ReadAsArray().flatten()
            data = self.get_vfd(data)
            for j, v in enumerate(data):
                if v < 0.05:
                    data[j] = 0
                elif v >= 0.05 and v < 0.15:
                    data[j] = 1
                elif v >= 0.15 and v < 0.3:
                    data[j] = 2
                elif v >= 0.3 and v < 0.6:
                    data[j] = 3
                else:
                    data[j] = 4
            data = data.astype(np.int8)
            imgs.append(data)
            self.write_img(out_path + file, proj, geotrans,
                           data.reshape(width, height))
            # print(file + ' is done!')
        return imgs, files
    
    def writeChange(self, reclass_path, change_path):
        files = os.listdir(reclass_path)
        files = list(filter(self.file_filter, files))  # 筛选tif
        files.sort()
        rate = []
        for i in range(self.n-1):
            img = gdal.Open(reclass_path + files[i])
            width = img.RasterXSize  # 栅格矩阵的列数
            height = img.RasterYSize  # 栅格矩阵的行数
            geotrans = img.GetGeoTransform()  # 仿射矩阵，左上角像素的大地坐标和像素分辨率
            proj = img.GetProjection()  # 地图投影信息，字符串表示
            data = img.ReadAsArray().flatten()
            next = gdal.Open(reclass_path + files[i+1]).ReadAsArray().flatten()
            change = []
            l = 0.0
            c = 0.0
            g = 0.0
            for j, v in enumerate(data):
                if v < next[j]:
                    change.append(1)  # 增加
                    g += 1
                elif v == next[j]:
                    change.append(0)  # 不变
                    c += 1
                else:
                    change.append(2)  # 减少
                    l += 1
            change = np.array(change, dtype=np.int8)
            self.write_img(change_path + self.files[i] + '.tif', proj, geotrans, change.reshape(width, height))
            rate.append([c / (c + g + l), g / (c + g + l), l / (c + g + l)])
        return rate

    def getInit(self, imgs, n):
        category = []
        for i in range(n):
            tmp = [0, 0, 0, 0, 0]
            for v in imgs[i]:
                if v == 0:
                    tmp[0] += 1
                elif v == 1:
                    tmp[1] += 1
                elif v == 2:
                    tmp[2] += 1
                elif v == 3:
                    tmp[3] += 1
                else:
                    tmp[4] += 1
            category.append(tmp)
        category = np.array(category, dtype='float')
        return category

    def getVar(self, imgs, n):
        var = []
        for i in range(n-1):
            tmp = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [
                0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
            change = []
            for j, _ in enumerate(imgs[i]):
                tmp[imgs[i][j]][imgs[i+1][j]] += 1
            var.append(tmp)
        var = np.array(var, dtype='float')
        return var

    # category 1
    def S_U(self):
        S = []
        U = 0.0
        span = 0
        for i in range(self.n-1):
            S.append(sum(np.abs(
                self.category[i+1] - self.category[i])) / sum(self.category[i]) / (int(self.files[i][5:9]) - int(self.files[i][0:4])) * 100)
            U += sum(np.abs(self.category[i+1] - self.category[i]))
            span += int(self.files[i][5:9]) - int(self.files[i][0:4])
        U = U / sum(self.category[0]) / span * 100
        return S, U

    def area_S(self):
        S = []
        for i in range(self.n-1):
            S.append(
                sum(np.abs(self.category[i+1] - self.category[i])) / (int(self.files[i][5:9]) - int(self.files[i][0:4])))
        return S

    # category 2
    def GL(self):
        G = []
        L = []
        UG = []
        UL = []
        for i in range(self.n-1):
            tmpG = np.empty((5, 1), dtype='float')
            tmpL = np.empty((5, 1), dtype='float')
            for j in range(5):
                tmpG[j] = self.increase[i][j] / (int(self.files[i][5:9]) - int(self.files[i][0:4])) / self.category[i+1][j] * 100
                tmpL[j] = self.decrease[i][j] / (int(self.files[i][5:9]) - int(self.files[i][0:4])) / self.category[i][j] * 100
            G.append(tmpG)
            L.append(tmpL)
        for i in range(self.n-1):
            UG.append(np.sum(self.increase[i]) /
                      sum(self.category[i]) / (int(self.files[i][5:9]) - int(self.files[i][0:4])) * 100)
            UL.append(np.sum(self.decrease[i]) /
                      sum(self.category[i]) / (int(self.files[i][5:9]) - int(self.files[i][0:4])) * 100)

        return G, L, UG, UL

    def area_GL(self):
        G = []
        L = []
        for i in range(self.n-1):
            tmpG = np.empty((5, 1), dtype='float')
            tmpL = np.empty((5, 1), dtype='float')
            for j in range(5):
                tmpG[j] = self.increase[i][j] / (int(self.files[i][5:9]) - int(self.files[i][0:4]))
                tmpL[j] = self.decrease[i][j] / (int(self.files[i][5:9]) - int(self.files[i][0:4]))
            G.append(tmpG)
            L.append(tmpL)
        return G, L

    def get_files(self):
        return self.files

    def get_n(self):
        return self.n

    def get_rate(self):
        return self.rate

    # category 3
    # def RWQV(self):
    #     R_spring_summer = np.empty((5, 5), dtype='float')
    #     R_summer_autumn = np.empty((5, 5), dtype='float')
    #     R_autumn_winter = np.empty((5, 5), dtype='float')
    #     W_spring_summer = np.empty((5, 1), dtype='float')
    #     W_summer_autumn = np.empty((5, 1), dtype='float')
    #     W_autumn_winter = np.empty((5, 5), dtype='float')
    #     Q_spring_summer = np.empty((5, 5), dtype='float')
    #     Q_summer_autumn = np.empty((5, 5), dtype='float')
    #     Q_autumn_winter = np.empty((5, 5), dtype='float')
    #     V_spring_summer = np.empty((5, 1), dtype='float')
    #     V_summer_autumn = np.empty((5, 1), dtype='float')
    #     V_autumn_winter = np.empty((5, 5), dtype='float')
    #     for i in range(5):
    #         for j in range(5):
    #             if i == j:
    #                 continue
    #             R_spring_summer[i][j] = self.var_spring_summer[i][j] / \
    #                 self.season_month / self.category_spring[i] * 100
    #             R_summer_autumn[i][j] = self.var_summer_autumn[i][j] / \
    #                 self.season_month / self.category_summer[i] * 100
    #             R_autumn_winter[i][j] = self.var_autumn_winter[i][j] / \
    #                 self.season_month / self.category_autumn[i] * 100
    #             Q_spring_summer[i][j] = self.var_spring_summer[i][j] / \
    #                 self.season_month / self.category_summer[j] * 100
    #             Q_summer_autumn[i][j] = self.var_summer_autumn[i][j] / \
    #                 self.season_month / self.category_autumn[j] * 100
    #             Q_autumn_winter[i][j] = self.var_autumn_winter[i][j] / \
    #                 self.season_month / self.category_winter[j] * 100
    #         W_spring_summer[i] = self.increase_spring_summer[i] / self.season_month / (
    #             np.sum(self.category_spring) - self.category_spring[i]) * 100
    #         W_summer_autumn[i] = self.increase_summer_autumn[i] / self.season_month / (
    #             np.sum(self.category_summer) - self.category_summer[i]) * 100
    #         W_autumn_winter[i] = self.increase_autumn_winter[i] / self.season_month / (
    #             np.sum(self.category_autumn) - self.category_autumn[i]) * 100
    #         V_spring_summer[i] = self.decrease_spring_summer[i] / self.season_month / (
    #             np.sum(self.category_summer) - self.category_summer[i]) * 100
    #         V_summer_autumn[i] = self.decrease_summer_autumn[i] / self.season_month / (
    #             np.sum(self.category_autumn) - self.category_autumn[i]) * 100
    #         V_autumn_winter[i] = self.decrease_autumn_winter[i] / self.season_month / (
    #             np.sum(self.category_winter) - self.category_winter[i]) * 100

    #     return R_spring_summer, R_summer_autumn, R_autumn_winter, W_spring_summer, W_summer_autumn, W_autumn_winter, Q_spring_summer, Q_summer_autumn, Q_autumn_winter, V_spring_summer, V_summer_autumn, V_autumn_winter
