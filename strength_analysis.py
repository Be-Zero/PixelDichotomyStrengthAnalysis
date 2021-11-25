import numpy as np


class strength_analysis:
    # init
    def __init__(self):
        self.category_80s = np.array([1650, 621, 2271, 4542, 6056], dtype='double')
        self.category_90s = np.array([1637, 634, 2271, 4542, 6056], dtype='double')
        self.category_00s = np.array([1853, 418, 2271, 4542, 6056], dtype='double')
        self.years_80s_90s = 10
        self.years_90s_00s = 6
        self.years_80s_00s = 16
        self.var_80s_90s = np.array([[1551, 99, 0, 0, 0], [84, 457, 80, 0, 0], [2, 78, 2137, 54, 0], [0, 0, 54, 4313, 175],
                                [0, 0, 0, 175, 5881]], dtype='double')
        self.var_90s_00s = np.array([[1616, 21, 0, 0, 0], [229, 332, 73, 0, 0], [8, 65, 2124, 74, 0], [0, 0, 74, 4251, 217],
                                [0, 0, 0, 217, 5839]], dtype='double')
        self.increase_80s_90s = np.array([86, 177, 134, 229, 175], dtype='double')
        self.increase_90s_00s = np.array([237, 86, 147, 291, 217], dtype='double')
        self.decrease_80s_90s = np.array([99, 164, 134, 229, 175], dtype='double')
        self.decrease_90s_00s = np.array([21, 302, 147, 291, 217], dtype='double')

    # category 1
    def S_U(self):
        S_80s_90s = np.sum(np.abs(self.category_90s - self.category_80s)) / sum(self.category_80s) / self.years_80s_90s * 100
        S_90s_00s = sum(np.abs(self.category_00s - self.category_90s)) / sum(self.category_90s) / self.years_90s_00s * 100
        U = (sum(np.abs(self.category_90s - self.category_80s)) + sum(np.abs(self.category_00s - self.category_90s))) / sum(self.category_80s) / self.years_80s_00s * 100
        return S_80s_90s, S_90s_00s, U

    def area_S(self):
        S_80s_90s = np.sum(np.abs(self.category_90s - self.category_80s)) / self.years_80s_90s
        S_90s_00s = sum(np.abs(self.category_00s - self.category_90s)) / self.years_90s_00s
        return S_80s_90s, S_90s_00s

    # category 2
    def GL(self):
        G_80s_90s = np.empty((5, 1), dtype='double')
        G_90s_00s = np.empty((5, 1), dtype='double')
        L_80s_90s = np.empty((5, 1), dtype='double')
        L_90s_00s = np.empty((5, 1), dtype='double')
        for i in range(5):
            G_80s_90s[i] = self.increase_80s_90s[i] / self.years_80s_90s / self.category_90s[i] * 100
            G_90s_00s[i] = self.increase_90s_00s[i] / self.years_90s_00s / self.category_00s[i] * 100
            L_80s_90s[i] = self.decrease_80s_90s[i] / self.years_80s_90s / self.category_80s[i] * 100
            L_90s_00s[i] = self.decrease_90s_00s[i] / self.years_90s_00s / self.category_90s[i] * 100
        U1 = np.sum(self.increase_80s_90s) / sum(self.category_80s) / self.years_80s_90s * 100
        U2 = np.sum(self.increase_90s_00s) / sum(self.category_90s) / self.years_90s_00s * 100
        return G_80s_90s, G_90s_00s, L_80s_90s, L_90s_00s, U1, U2

    def area_GL(self):
        G_80s_90s = np.empty((5, 1), dtype='double')
        G_90s_00s = np.empty((5, 1), dtype='double')
        L_80s_90s = np.empty((5, 1), dtype='double')
        L_90s_00s = np.empty((5, 1), dtype='double')
        for i in range(5):
            G_80s_90s[i] = self.increase_80s_90s[i] / self.years_80s_90s
            G_90s_00s[i] = self.increase_90s_00s[i] / self.years_90s_00s
            L_80s_90s[i] = self.decrease_80s_90s[i] / self.years_80s_90s
            L_90s_00s[i] = self.decrease_90s_00s[i] / self.years_90s_00s
        return G_80s_90s, G_90s_00s, L_80s_90s, L_90s_00s

    # category 3
    def RWQV(self):
        R_80s_90s = np.empty((5, 5), dtype='double')
        R_90s_00s = np.empty((5, 5), dtype='double')
        W_80s_90s = np.empty((5, 1), dtype='double')
        W_90s_00s = np.empty((5, 1), dtype='double')
        Q_80s_90s = np.empty((5, 5), dtype='double')
        Q_90s_00s = np.empty((5, 5), dtype='double')
        V_80s_90s = np.empty((5, 1), dtype='double')
        V_90s_00s = np.empty((5, 1), dtype='double')
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                R_80s_90s[i][j] = self.var_80s_90s[i][j] / self.years_80s_90s / self.category_80s[i] * 100
                R_90s_00s[i][j] = self.var_90s_00s[i][j] / self.years_90s_00s / self.category_90s[i] * 100
                Q_80s_90s[i][j] = self.var_80s_90s[i][j] / self.years_80s_90s / self.category_90s[j] * 100
                Q_90s_00s[i][j] = self.var_90s_00s[i][j] / self.years_90s_00s / self.category_00s[j] * 100
            W_80s_90s[i] = self.increase_80s_90s[i] / self.years_80s_90s / (np.sum(self.category_80s) - self.category_80s[i]) * 100
            W_90s_00s[i] = self.increase_90s_00s[i] / self.years_90s_00s / (np.sum(self.category_90s) - self.category_90s[i]) * 100
            V_80s_90s[i] = self.decrease_80s_90s[i] / self.years_80s_90s / (np.sum(self.category_90s) - self.category_90s[i]) * 100
            V_90s_00s[i] = self.decrease_90s_00s[i] / self.years_90s_00s / (np.sum(self.category_00s) - self.category_00s[i]) * 100

        return R_80s_90s, R_90s_00s, W_80s_90s, W_90s_00s, Q_80s_90s, Q_90s_00s, V_80s_90s, V_90s_00s