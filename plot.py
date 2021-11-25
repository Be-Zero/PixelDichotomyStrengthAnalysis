# coding=utf-8

from strength_analysis import *
import numpy
import matplotlib.pyplot as plt


SA = strength_analysis()

# plot 1
plt.clf()
S_80s_90s, S_90s_00s = SA.area_S()
plt.subplot(1, 2, 1)
plt.title('change area')
plt.xlabel("years") # 变化面积
plt.ylabel("change area") # 变化面积
plt.xlim(0, 5)
plt.xticks([1, 3], ['80s-90s', '90s-00s'])
plt.bar([1, 3], [S_80s_90s, S_90s_00s], color=['blue', 'green'], width=0.7)
plt.tight_layout()

# plot 2
S_80s_90s, S_90s_00s, U = SA.S_U()
plt.subplot(1, 2, 2)
plt.title('change rate')
plt.xlabel("change rate") # 变化率
plt.ylabel("percent") # 变化面积
plt.xlim(0, 5)
plt.xticks([1, 3], ['80s-90s', '90s-00s'])
plt.bar([1, 3], [S_80s_90s, S_90s_00s], color=['blue', 'green'], width=0.7)
plt.axhline(U, linestyle='--', c='red', label=str(U))
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()

# plot 3
plt.clf()
G_80s_90s, G_90s_00s, L_80s_90s, L_90s_00s = SA.area_GL()
plt.subplot(1, 2, 1)
plt.title('80s-90s increase area')
plt.xlabel("class") # 变化面积
plt.ylabel("area") # 变化面积
plt.xlim(0, 6)
plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
plt.bar([1, 2, 3, 4, 5], G_80s_90s, color=['blue', 'green'], width=0.5)
plt.tight_layout()
# plt.show()

# plot 4
G_80s_90s, G_90s_00s, L_80s_90s, L_90s_00s, U1, U2 = SA.GL()
plt.subplot(1, 2, 2)
plt.title('80s-90s increase rate')
plt.xlabel("class") # 变化率
plt.ylabel("rate") # 变化面积
plt.xlim(0, 6)
plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
plt.bar([1, 2, 3, 4, 5], G_80s_90s, color=['blue', 'green'], width=0.5)
plt.axhline(U1, linestyle='--', c = 'red', label=str(U1))
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()

# plot 5
plt.clf()
G_80s_90s, G_90s_00s, L_80s_90s, L_90s_00s = SA.area_GL()
plt.subplot(1, 2, 1)
plt.title('90s-00s increase area')
plt.xlabel("class") # 变化率
plt.ylabel("area") # 变化面积
plt.xlim(0, 6)
plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
plt.bar([1, 2, 3, 4, 5], G_90s_00s, color=['blue', 'green'], width=0.5)
plt.tight_layout()
# plt.show()

# plot 6
G_80s_90s, G_90s_00s, L_80s_90s, L_90s_00s, U1, U2 = SA.GL()
plt.subplot(1, 2, 2)
plt.title('90s-00s increase rate')
plt.xlabel("class") # 变化率
plt.ylabel("rate") # 变化面积
plt.xlim(0, 6)
plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
plt.bar([1, 2, 3, 4, 5], G_90s_00s, color=['blue', 'green'], width=0.5)
plt.axhline(U1, linestyle='--', c = 'red', label=str(U1))
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()

# plot 7
plt.clf()
G_80s_90s, G_90s_00s, L_80s_90s, L_90s_00s = SA.area_GL()
plt.subplot(1, 2, 1)
plt.title('80s-90s decrease area')
plt.xlabel("class") # 变化率
plt.ylabel("area") # 变化面积
plt.xlim(0, 6)
plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
plt.bar([1, 2, 3, 4, 5], L_80s_90s, color=['blue', 'green'], width=0.5)
plt.tight_layout()
# plt.show()

# plot 8
G_80s_90s, G_90s_00s, L_80s_90s, L_90s_00s, U1, U2 = SA.GL()
plt.subplot(1, 2, 2)
plt.title('80s-90s decrease rate')
plt.xlabel("class") # 变化率
plt.ylabel("rate") # 变化面积
plt.xlim(0, 6)
plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
plt.bar([1, 2, 3, 4, 5], L_80s_90s, color=['blue', 'green'], width=0.5)
plt.axhline(U2, linestyle='--', c = 'red', label=str(U2))
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()

# plot 9
plt.clf()
G_80s_90s, G_90s_00s, L_80s_90s, L_90s_00s = SA.area_GL()
plt.subplot(1, 2, 1)
plt.title('90s-00s decrease area')
plt.xlabel("class") # 变化率
plt.ylabel("area") # 变化面积
plt.xlim(0, 6)
plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
plt.bar([1, 2, 3, 4, 5], L_90s_00s, color=['blue', 'green'], width=0.5)
plt.tight_layout()
# plt.show()

# plot 10
G_80s_90s, G_90s_00s, L_80s_90s, L_90s_00s, U1, U2 = SA.GL()
plt.subplot(1, 2, 2)
plt.title('90s-00s decrease rate')
plt.xlabel("class") # 变化率
plt.ylabel("rate") # 变化面积
plt.xlim(0, 6)
plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
plt.bar([1, 2, 3, 4, 5], L_90s_00s, color=['blue', 'green'], width=0.5)
plt.axhline(U2, linestyle='--', c = 'red', label=str(U2))
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()

R_80s_90s, R_90s_00s, W_80s_90s, W_90s_00s, Q_80s_90s, Q_90s_00s, V_80s_90s, V_90s_00s = SA.RWQV()
for i in range(5):
    for j in range(5):
        if i == j:
            continue
        print "R_90s_00s[{}][{}]:{}".format(i, j, R_90s_00s[i][j]) # 4 to 5