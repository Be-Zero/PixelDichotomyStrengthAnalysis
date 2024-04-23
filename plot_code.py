# coding=utf-8

import os

import matplotlib.pyplot as plt
import numpy as np

from strengthAnalysis import strengthAnalysis

if __name__ == '__main__':
    in_path = "E:/project/pixelDichotomyStrengthAnalysis/data/1/"  # 用户上传n张图到文件夹，要求命名为年份
    fig_path = in_path + "figs/"  # 本程序画图示例，用前端界面时不需要该文件夹
    if os.path.exists(fig_path) == False:
        os.mkdir(fig_path)
    SA = strengthAnalysis(in_path, mode='debug')  # 创建对象，main模式为标准模式，debug为测试
    
    rate = SA.get_rate()  # 获取变化比率，对应change文件夹内的图像，前端可以做个图例
    files = SA.get_files()

    for i in range(SA.get_n()-1):
        print('\n{} 时间段内变化情况：'.format(files[i]))
        print('    覆盖度类型保持不变：{:.2f}%'.format(rate[i][0] * 100))
        print('    覆盖度类型由低变高：{:.2f}%'.format(rate[i][1] * 100))
        print('    覆盖度类型由高变低：{:.2f}%\n'.format(rate[i][2] * 100))

    # plot 1 画每一年变化面积（单位为像元）
    plt.clf()
    S = SA.area_S()  # 获取S，有n个元素的列表，每个元素代表第i个年份植被覆盖类型变化数量
    plt.subplot(1, 2, 1)
    plt.title('change area')
    plt.xlabel("years")  # 变化面积
    plt.ylabel("change area")  # 变化面积
    # plt.ylim(0, 20)
    # plt.xlim(0, 10)
    plt.xticks([i*20 for i in range(1, SA.get_n())], SA.get_files())  # SA.get_n()就是获取n（年份个数），SA.get_files()就是获取n-1个时间段的命名（如：2017_2018）
    plt.bar([i*20 for i in range(1, SA.get_n())], S, color=[
            'blue', 'green', 'yellow'], width=10)
    plt.tight_layout()
    # plt.show()

    # plot 2 画每一年变化比率
    S, U = SA.S_U()  # S表示有n个元素的列表，每个元素代表第i个年份植被覆盖类型变化比率，U表示均值线，反应变化的平均强度，超过U为剧烈，反之为平缓
    plt.subplot(1, 2, 2)
    plt.title('change rate')
    plt.xlabel("change rate")  # 变化率
    plt.ylabel("percent")  # 变化面积
    # plt.xlim(0, 10)
    # plt.ylim(0, 0.000020)
    plt.xticks([i*20 for i in range(1, SA.get_n())], SA.get_files())
    plt.bar([i*20 for i in range(1, SA.get_n())], S, color=[
            'blue', 'green', 'yellow'], width=10)
    plt.axhline(U, linestyle='--', c='red', label=str(U))
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(fig_path + 'change.png')
    # plt.show()

    # plot 3 画每个时段不同覆盖类型增加面积（单位为像元）
    areaG, areaL = SA.area_GL()  # 获取不同覆盖类型增加和减少像元数量的list，维度为(n-1)*5*1，表示n-1个时间段内5中类别的增减情况，G为增，L为减
    G, L, UG, UL = SA.GL()  # 原理同上，表示的是变化比率，维度(n-1)*5*1，UG和UL表示增减程度的均值线，反应变化的平均强度，超过U为剧烈，反之为平缓
    files = SA.get_files()
    for i in range(SA.get_n()-1):
        plt.clf()
        plt.subplot(1, 2, 1)
        plt.title('{} increase area'.format(files[i]))
        plt.xlabel("class")  # 变化面积
        plt.ylabel("pixcel")  # 变化面积
        # plt.xlim(0, 6)
        plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
        plt.bar([1, 2, 3, 4, 5], areaG[i].flatten(),
                color=['blue', 'green'], width=0.5)
        plt.tight_layout()
        # plt.show()

        # plot 4 画每个时段不同覆盖类型增加比率
        plt.subplot(1, 2, 2)
        plt.title('{} increase rate'.format(files[i]))
        plt.xlabel("class")  # 变化率
        plt.ylabel("rate")  # 变化面积
        # plt.xlim(0, 6)
        plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
        plt.bar([1, 2, 3, 4, 5], G[i].flatten(),
                color=['blue', 'green'], width=0.5)
        plt.axhline(UG[i], linestyle='--', c='red', label=str(UG[i]))
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(fig_path + '{}_G.png'.format(files[i]))
        # plt.show()

        # plot 5 画每个时段不同覆盖类型减少面积（单位为像元）
        plt.clf()
        plt.subplot(1, 2, 1)
        plt.title('{} decrease area'.format(files[i]))
        plt.xlabel("class")  # 变化率
        plt.ylabel('number of pixels')  # 变化面积
        # plt.xlim(0, 6)
        plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
        plt.bar([1, 2, 3, 4, 5], areaL[i].flatten(),
                color=['blue', 'green'], width=0.5)
        plt.tight_layout()
        # plt.show()

        # plot 6 画每个时段不同覆盖类型减少比率
        plt.subplot(1, 2, 2)
        plt.title('{} decrease rate'.format(files[i]))
        plt.xlabel("class")  # 变化率
        plt.ylabel("rate")  # 变化面积
        # plt.xlim(0, 6)
        plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
        plt.bar([1, 2, 3, 4, 5], L[i].flatten(),
                color=['blue', 'green'], width=0.5)
        plt.axhline(UL[i], linestyle='--', c='red', label=str(UL[i]))
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(fig_path + '{}_L.png'.format(files[i]))
        # plt.show()
