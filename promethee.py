import numpy as np


class Promethee:
    def get_brut_matrix(self, mp):
        return mp[2:, 1:].astype(float)

    def get_max_col(self, mp):
        return mp.max(0)

    def get_min_col(self, mp):
        return mp.min(0)

    def get_weights(self, mp):
        return mp[1:2, 1:][0].astype(float)

    def get_devs(self, mp):
        return np.concatenate(mp[2:, 0:1])

    def get_normalized_matrix(self, brut_mp):
        num_rows, num_cols = brut_mp.shape
        max = self.get_max_col(brut_mp)
        min = self.get_min_col(brut_mp)

        for i in range(num_cols):
            for j in range(num_rows):
                brut_mp[j, i] = (brut_mp[j, i] - min[i])/(max[i]-min[i])

        # for i in range(num_cols):
        #     if(True):
        #         # Benifit Criteria
        #         brut_mp[0:, i:i+1] = (brut_mp[0:, i:i+1] -
        #                               min[i])/(max[i]-min[i])
        #     # else:
        #     # Cost Criteria
        #     #     brut_mp[0:, i:i+1] = (max[i]-brut_mp[0:,
        #     #                           i:i+1])/(max[i]-min[i])

        return brut_mp

    def pairwise_comp_matrix(self, normal_matrix):
        row_count, col_count = normal_matrix.shape
        new_row_count = row_count*(row_count-1)

        pw_m = np.zeros([new_row_count, col_count])
        for i in range(col_count):
            m = 0
            for j in range(row_count):
                for k in range(row_count):
                    if (j != k):
                        pw_m[m, i] = normal_matrix[j, i] - normal_matrix[k, i]
                        m = m+1
        return pw_m

    def preference_func_array(self, pairwise_matrix):
        with np.nditer(pairwise_matrix, op_flags=['readwrite']) as values:
            for value in values:
                if (value < 0):
                    value[...] = 0
        return pairwise_matrix

    def preference_func_array_weights(self, preference_func_martix, mp):
        num_cols = preference_func_martix.shape[1]
        num_rows = preference_func_martix.shape[0]
        weights = self.get_weights(mp)
        for col in range(num_cols):
            for row in range(num_rows):
                preference_func_martix[row,
                                       col] = preference_func_martix[row, col]*weights[col]
        return preference_func_martix

    def sum_preference_matrix_weights_rows(self, mp):
        return np.sum(mp, axis=1)

    def squar_pref_index(self, mp,  sum_pref_m):
        row_num = mp.shape[0]
        mp1 = np.zeros([row_num, row_num])
        k = 0
        for i in range(row_num):
            for j in range(row_num):
                if (i == j):
                    mp1[j, i] = 0
                else:
                    mp1[i, j] = sum_pref_m[k]
                    k = k + 1
        return mp1

    def pos_flow(self, squared_m):
        index = squared_m.shape[0]
        row_sum = np.sum(squared_m, axis=1)
        pos_flow = row_sum/(index-1)
        return pos_flow

    def neg_flow(self, squared_m):
        index = squared_m.shape[0]
        col_sum = np.sum(squared_m, axis=0)
        neg_flow = col_sum/(index-1)
        return neg_flow

    def net_flow(self, pos_flow, neg_flow):
        return pos_flow-neg_flow

    def sorted_devs(self, mp, net_flow):
        devs_matrix = self.get_devs(mp)
        num_devs = net_flow.shape[0]
        devs_dict = {}
        for i in range(num_devs):
            devs_dict[devs_matrix[i]] = net_flow[i]
        sorted_dict = sorted(devs_dict.items(), key=lambda x: x[1])
        return sorted_dict


if __name__ == '__main__':
    # Format numpy print
    float_formatter = "{:.6f}".format
    np.set_printoptions(formatter={'float_kind': float_formatter})

    mp = np.array([["Actions", "Grade", "Vélocité", "Commitment"],
                   ["Weights", 0.2, 0.5, 0.3],
                   ["Dev1", 3, 4, 3],
                   ["Dev2", 2, 4, 0],
                   ["Dev3", 5, 9, 4],
                   ["Dev4", 2, 10, 2],
                   ["Dev5", 4, 5, 0],
                   ["Dev6", 1, 1, 0],
                   ["Dev7", 5, 10, 2]])

    # mp1 = np.array([["Actions", "Critère 1", "Critère 2", "Critère 3", "Critère 4", "Critère 5", "Critère 6"],
    #                ["Weights", 0.2336, 0.1652, 0.3355, 0.1021, 0.0424, 0.1212],
    #                ["Action 1", 1350, 1850, 7.5, 2.58, 93.5, 0.045],
    #                ["Action 2", 1680, 1650, 8.5, 3.75, 95.3, 0.068],
    #                ["Action 3", 1560, 1950, 6.5, 4.86, 88.6, 0.095],
    #                ["Action 4", 1470, 1850, 9.5, 3.16, 98.4, 0.072]])

    promethee = Promethee()
    mp_brut_float = promethee.get_brut_matrix(mp)
    print("===============================================================")
    print("Brut Matrix")
    print(mp_brut_float)

    print("===============================================================")
    print("Normalized Matrix")
    normal_matrix = promethee.get_normalized_matrix(mp_brut_float)
    print(normal_matrix)

    print("===============================================================")
    print("Pairwise Matrix")
    pairwise_matrix = promethee.pairwise_comp_matrix(normal_matrix)
    print(pairwise_matrix)

    print("===============================================================")
    print("Preference func Martix")
    preference_func_martix = promethee.preference_func_array(pairwise_matrix)
    print(preference_func_martix)

    print("===============================================================")
    print("Preference func Martix with weights")
    preference_func_martix_weights = promethee.preference_func_array_weights(
        preference_func_martix, mp)
    print(preference_func_martix_weights)

    print("===============================================================")
    print("Sum Preference func Martix with weights Rows")
    sum_preference_matrix_weights_rows = promethee.sum_preference_matrix_weights_rows(
        preference_func_martix_weights)
    print(sum_preference_matrix_weights_rows)

    print("===============================================================")
    print("Sum Preference Martix Squared")
    squared = promethee.squar_pref_index(
        mp_brut_float, sum_preference_matrix_weights_rows)
    print(squared)

    print("===============================================================")
    print("Positif Flow")
    pos_flow = promethee.pos_flow(squared)
    print(pos_flow)

    print("===============================================================")
    print("Negatif Flow")
    neg_flow = promethee.neg_flow(squared)
    print(neg_flow)

    print("===============================================================")
    print("Net Flow")
    net_flow = promethee.net_flow(pos_flow, neg_flow)
    print(net_flow)

    print("===============================================================")
    print("Sorted Developpers")
    sorted_devs = promethee.sorted_devs(mp, net_flow)
    print(sorted_devs)
