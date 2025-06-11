from lab2_4 import fill_matrix, find_C, find_Tavg, t_mult, t_diff, t_sum, t_comparison, t_div
from lab2_4 import A, B, E, G, C, Tn, p, q, m, sum_call, mult_call, diff_call, compare_call, div_call, n, Tavg



def main_graphicsKr():
    import matplotlib.pyplot as plt

    global p, q, m, Tn, sum_call, mult_call, diff_call, div_call, compare_call, n, Tavg
    t_mult, t_diff, t_sum, t_comparison, t_diff = 1, 1, 1, 1, 1  # задаём времена операций
    ky_n10 = []
    ky_n7 = []
    r_vals = []

    for i in range(20):
        # --- n = 10 ---
        Tn, Tavg = 0, 0
        sum_call, mult_call, diff_call, compare_call, div_call = 0, 0, 0, 0, 0
        m = p = q = i + 1
        n = 10
        fill_matrix(m, p, q)
        find_C(p, q, m)
        r = p * q + q * m + p * m + m + p * q
        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + div_call * t_diff
        Ky = T1 / Tn
        ky_n10.append(Ky)
        print(f"n = {n}, m = {m}, r = {r}, T1 = {T1}, Tn = {Tn}, Ky = {Ky}")
        r_vals.append(r)

    for i in range(20):
        # --- n = 7 ---
        Tn, Tavg = 0, 0
        sum_call, mult_call, diff_call, compare_call, div_call = 0, 0, 0, 0, 0
        m = p = q = i + 1
        n = 7
        fill_matrix(m, p, q)
        find_C(p, q, m)
        # r = p * q + q * m + p * m + m + p * q
        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + t_div * div_call
        Ky = T1 / Tn
        print(f"n = {n}, m = {m}, r = {r}, T1 = {T1}, Tn = {Tn}, Ky = {Ky}")
        ky_n7.append(Ky)

    plt.figure(figsize=(10, 5))
    plt.plot(r_vals, ky_n10, 'k', label='n = 10', linewidth=2)
    plt.plot(r_vals, ky_n7, label='n = 7', linewidth=3)
    plt.xlabel('r', fontsize=14)
    plt.ylabel('Ky(r)', fontsize=14)
    plt.grid(True)
    plt.legend(loc='best', fontsize=12)
    plt.show()


def main_graphicsKyn():
    import matplotlib.pyplot as plt

    global p, q, m, Tn, sum_call, mult_call, diff_call, compare_call, div_call, n, Tavg
    t_mult, t_diff, t_sum, t_comparison, t_diff = 1, 1, 1, 1, 1
    x = []
    ky_40 = []

    for n in range(1, 51):
        found = False
        for p in range(1, 11):
            for q in range(1, 11):
                for m in range(1, 11):
                    r = p * q + q * m + p * m + m + p * q
                    if r == 40:
                        Tn, Tavg = 0, 0
                        sum_call, mult_call, diff_call, compare_call, div_call = 0, 0, 0, 0, 0
                        fill_matrix(m, p, q)
                        find_C(p, q, m)
                        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + div_call * t_div
                        Ky = T1 / Tn
                        # print(f"n = {n}, m = {m}, r = {r}, T1 = {T1}, Tn = {Tn}, Ky = {Ky}")
                        ky_40.append(Ky)
                        x.append(n)
                        found = True
                        break
                if found:
                    break
            if found:
                break

    x2 = []  # значения n для r = 33
    ky_33 = []

    for n in range(1, 51):
        found = False
        for p in range(1, 11):
            for q in range(1, 11):
                for m in range(1, 11):
                    r = p * q + q * m + p * m + m + p * q
                    if r == 33:
                        Tn, Tavg = 0, 0
                        sum_call, mult_call, diff_call, compare_call, div_call = 0, 0, 0, 0, 0
                        fill_matrix(m, p, q)
                        find_C(p, q, m)
                        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + div_call * t_diff
                        Ky = T1 / Tn
                        # print(f"n = {n}, m = {m}, r = {r}, T1 = {T1}, Tn = {Tn}, Ky = {Ky}")
                        ky_33.append(Ky)
                        x2.append(n)
                        found = True
                        break
                if found:
                    break
            if found:
                break

    # Построение графика
    plt.figure(figsize=(10, 5))
    # print(ky_40)
    # print(ky_33)
    plt.plot(x, ky_40, 'k', label='r = 40', linewidth=2)
    plt.plot(x2, ky_33, label='r = 33', linewidth=3)
    plt.xlabel('n', fontsize=14)
    plt.ylabel('Ky(n)', fontsize=14)
    plt.grid(True)
    plt.legend(loc='best', fontsize=12)
    plt.show()


def main_graphicsEr():
    import matplotlib.pyplot as plt

    global p, q, m, Tn, sum_call, mult_call, diff_call, div_call, compare_call, n, Tavg
    t_mult, t_diff, t_sum, t_comparison, t_div = 1, 1, 1, 1, 1  # задаём времена операций
    e_n7 = []
    e_n10 = []
    r_vals = []

    for i in range(20):
        # --- n = 10 ---
        Tn, Tavg = 0, 0
        sum_call, mult_call, diff_call, compare_call, div_call = 0, 0, 0, 0, 0
        m = p = q = i + 1
        n = 10
        fill_matrix(m, p, q)
        find_C(p, q, m)
        r = p * q + q * m + p * m + m + p * q
        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + div_call * t_div
        Ky = T1 / Tn
        e = Ky / n
        # print(f"n = {n}, m = {m}, r = {r}, T1 = {T1}, Tn = {Tn}, Ky = {Ky}, e = {e}")
        e_n10.append(e)
        r_vals.append(r)

    for i in range(20):
        # --- n = 7 ---
        Tn, Tavg = 0, 0
        sum_call, mult_call, diff_call, compare_call, div_call = 0, 0, 0, 0, 0
        m = p = q = i + 1
        n = 7
        fill_matrix(m, p, q)
        find_C(p, q, m)
        r = p * q + q * m + p * m + m + p * q
        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + div_call * t_div
        Ky = T1 / Tn
        e = Ky / n
        # print(f"n = {n}, m = {m}, r = {r}, T1 = {T1}, Tn = {Tn}, Ky = {Ky}, e = {e}")
        e_n7.append(e)

    plt.figure(figsize=(10, 5))
    plt.plot(r_vals, e_n10, 'k', label='n = 10', linewidth=2)
    plt.plot(r_vals, e_n7, label='n = 7', linewidth=3)
    plt.xlabel('r', fontsize=14)
    plt.ylabel('e(r)', fontsize=14)
    plt.grid(True)
    plt.legend(loc='best', fontsize=12)
    plt.show()


def main_graphicsEn():
    import matplotlib.pyplot as plt

    global p, q, m, Tn, sum_call, mult_call, diff_call, compare_call, n, Tavg, div_call
    t_mult, t_diff, t_sum, t_comparison, t_div = 1, 1, 1, 1, 1
    x = []   # значения n для r = 40
    e_40 = []

    for n in range(1, 51):
        found = False
        for p in range(1, 11):
            for q in range(1, 11):
                for m in range(1, 11):
                    r = p * q + q * m + p * m + m + p * q
                    if r == 40:
                        Tn, Tavg = 0, 0
                        sum_call, mult_call, diff_call, compare_call = 0, 0, 0, 0
                        fill_matrix(m, p, q)
                        find_C(p, q, m)
                        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + t_div * div_call
                        Ky = T1 / Tn if Tn != 0 else 0
                        e = Ky / n
                        e_40.append(e)
                        x.append(n)
                        found = True
                        break
                if found:
                    break
            if found:
                break

    x2 = []  # значения n для r = 33
    e_33 = []

    for n in range(1, 51):
        found = False
        for p in range(1, 11):
            for q in range(1, 11):
                for m in range(1, 11):
                    r = p * q + q * m + p * m + m + p * q
                    if r == 33:
                        Tn, Tavg = 0, 0
                        sum_call, mult_call, diff_call, compare_call, div_call = 0, 0, 0, 0, 0
                        fill_matrix(m, p, q)
                        find_C(p, q, m)
                        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + div_call * t_div
                        Ky = T1 / Tn if Tn != 0 else 0
                        e = Ky / n
                        e_33.append(e)
                        x2.append(n)
                        found = True
                        break
                if found:
                    break
            if found:
                break

    # Построение графика
    plt.figure(figsize=(10, 5))
    plt.plot(x, e_40, 'k', label='r = 40', linewidth=2)
    plt.plot(x2, e_33, label='r = 33', linewidth=3)
    plt.xlabel('n', fontsize=14)
    plt.ylabel('e(n)', fontsize=14)
    plt.grid(True)
    plt.legend(loc='best', fontsize=12)
    plt.show()


def main_graphicsDr():
    global p, q, m, Tn, sum_call, mult_call, diff_call, div_call,compare_call, n, Tavg
    x = []
    d_ = []
    ky_ = []

    for i in range(10):
        Tn, Tavg = 0, 0
        sum_call, mult_call, diff_call, compare_call, div_call = 0, 0, 0, 0, 0
        m = i + 1
        p = i + 1
        q = i + 1
        n = 10
        fill_matrix(int(m), int(p), int(q))
        find_C(int(p), int(q), int(m))
        r = p * q + q * m + p * m + 1 * m + p * q
        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + div_call * t_div
        Ky = T1 / Tn
        e = Ky / n
        Tavg = find_Tavg()
        Lavg = Tavg / r
        D = Tn / Lavg
        ky_.append(Ky)
        d_.append(D)
        x.append(r)
    y2 = []
    for i in range(10):
        Tn, Tavg = 0, 0
        sum_call, mult_call, diff_call, div_call,compare_call = 0, 0, 0, 0, 0
        m = i + 1
        p = i + 1
        q = i + 1
        n = 7
        fill_matrix(int(m), int(p), int(q))
        find_C(int(p), int(q), int(m))
        r = p * q + q * m + p * m + 1 * m + p * q
        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + t_div * div_call
        Ky = T1 / Tn
        e = Ky / n
        Tavg = find_Tavg()
        Lavg = Tavg / r
        D = Tn / Lavg
        ky_.append(Ky)
        y2.append(D)

    import matplotlib.pyplot as plt
    y = d_
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, 'k', label='n = 10', linewidth=2)
    plt.plot(x, y2, label="n = 7", linewidth=3)
    plt.xlabel('r', fontsize=14)
    plt.ylabel('D(r)', fontsize=14)
    plt.grid(True)
    plt.legend(loc='best', fontsize=12)
    plt.show()





def main_graphicsDn():
    global p, q, m, Tn, sum_call, mult_call, diff_call, div_call,compare_call, n, Tavg
    x = []
    d_ = []
    ky_ = []

    for n in range(1, 51):
        for p in range(1, 11):
            for q in range(1, 11):
                for m in range(1, 11):
                    Tn, Tavg = 0, 0
                    sum_call, mult_call, diff_call, compare_call, div_call =0, 0, 0, 0, 0
                    r = p * q + q * m + p * m + 1 * m + p * q
                    if r == 33:
                        fill_matrix(int(m), int(p), int(q))
                        find_C(int(p), int(q), int(m))
                        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + div_call * t_div
                        Ky = T1 / Tn
                        e = Ky / n
                        Tavg = find_Tavg()
                        Lavg = Tavg / r
                        D = Tn / Lavg
                        # print(f"n = {n}, r = {r}, m = {m}, Tn = {Tn}, Lavg = {Lavg}, D = {D}")
                        ky_.append(Ky)
                        d_.append(D)
                        x.append(n)
                        break  # Нашли подходящие p, q, m, выходим из цикла
                else:
                    continue
                break
            else:
                continue
            break

    y2 = []
    x2 = []
    for n in range(1, 51):
        for p in range(1, 11):
            for q in range(1, 11):
                for m in range(1, 11):
                    Tn, Tavg = 0, 0
                    sum_call, mult_call, diff_call, compare_call, div_call =0, 0, 0, 0, 0
                    r = p * q + q * m + p * m + 1 * m + p * q
                    if r == 40:
                        fill_matrix(int(m), int(p), int(q))
                        find_C(int(p), int(q), int(m))
                        T1 = mult_call * t_mult + diff_call * t_diff + sum_call * t_sum + compare_call * t_comparison + div_call * t_div
                        Ky = T1 / Tn
                        e = Ky / n
                        Tavg = find_Tavg()
                        Lavg = Tavg / r
                        D = Tn / Lavg
                        # print(f"n = {n}, r = {r}, m = {m}, Tn = {Tn}, Lavg = {Lavg}, D = {D}")
                        ky_.append(Ky)
                        y2.append(D)
                        x2.append(n)
                        break
                else:
                    continue
                break
            else:
                continue
            break

    import matplotlib.pyplot as plt
    y = d_
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, 'k', label='r = 33', linewidth=2)
    plt.plot(x2, y2, label="r = 40", linewidth=3)
    plt.xlabel('n', fontsize=14)
    plt.ylabel('D(n)', fontsize=14)
    plt.grid(True)
    plt.legend(loc='best', fontsize=12)
    plt.show()


    
# Для построения графиков раскомментируйте нужные строки
main_graphicsKr()
# main_graphicsKyn()
# main_graphicsEr()
# main_graphicsEn()
# main_graphicsDr()
# main_graphicsDn()
