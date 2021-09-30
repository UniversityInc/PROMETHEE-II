import numpy as np


class Promethee:
    def __init__(self, mp):
        self.mp = mp

    def get_brut_matrix(self, mp):
        return mp[2:, 1:].astype(float)

    def get_max_col(self, mp):
        return mp.max(0)

    def get_min_col(self, mp):
        return mp.min(0)

    def get_normalized_matrix(self, brut_mp):
        # Get number of columns, Max and Min value Of columns
        num_cols = mp.shape[0]
        max = self.get_max_col(brut_mp)
        min = self.get_min_col(brut_mp)

        for i in range(num_cols+1):
            if(True):
                # Benifit Criteria
                brut_mp[0:, i:i+1] = (brut_mp[0:, i:i+1] -
                                      min[i])/(max[i]-min[i])
            # else:
            # Cost Criteria
            #     brut_mp[0:, i:i+1] = (max[i]-brut_mp[0:,
            #                           i:i+1])/(max[i]-min[i])

        return brut_mp

    def pairwise_comp_matrix(self, mp):
        row_count, col_count = mp.shape
        new_row_count = row_count*(row_count-1)

        mp2 = np.zeros([new_row_count, col_count])
        for i in range(col_count):
            print(i)
            for j in range(row_count):
                print(j)
                m = 0
                print(m)
                for k in range(row_count):
                    print(k)
                    if (j != k):
                        mp2[i, m] = mp[i, j] - mp[k, i]
                        m = m+1
                        print(mp2)
        return mp2


if __name__ == '__main__':
    # Format numpy print
    float_formatter = "{:.6f}".format
    np.set_printoptions(formatter={'float_kind': float_formatter})

    mp = np.array([["Actions", "Grade", "Vélocité", "Commitment"],
                   ["Weights", 0.2, 0.5, 0.3],
                   ["Dev1", 3, 4, 3],
                   ["Dev2", 2, 4, 0],
                   ["Dev3", 5, 9, 4]])

    mp1 = np.array([[1350, 1850, 7.5, 2.58, 93.5, 0.045],
                   [1680, 1650, 8.5, 3.75, 95.3, 0.068],
                   [1560, 1950, 6.5, 4.86, 88.6, 0.095],
                   [1470, 1850, 9.5, 3.16, 98.4, 0.072]])

    promethee = Promethee(mp)
    mp_brut_float = promethee.get_brut_matrix(promethee.mp)
    print("Brut Matrix")
    print(mp1)
    print("===============================================================")
    print("Normalized Matrix")
    normal_matrix = promethee.get_normalized_matrix(mp1)
    print(normal_matrix)

    # x, y = mp1.shape
    # print(x)
    # x = x*(x-1)

    # mp2 = np.zeros([x, y])
    # print(mp2)
    print("===============================================================")
    print("Pairwise Matrix")
    print(promethee.pairwise_comp_matrix(normal_matrix))
