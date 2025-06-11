# Модели решения задач в интеллектуальных системах
# Лабораторная работа 2
# Вариант 4.    
# 221703, Демидовец Д.В.
# Дата: 10.05.2025
# Источники:  
# https://github.com/aleshkey/sisd
# В 2 ч. Ч.1: Формальные модели обработки информации и параллельные модели решения задач:
# учеб.-метод. пособие/ В. П. Ивашенко. – Минск : БГУИР, 2020. – 79 с.


import random
import math

ALFABET = [str(i) for i in range(10)]
A, B, E, G, C = [], [], [], [], []
Tn = 0
p, q, m = 0, 0, 0
sum_count, mult_count, diff_count, compare_count, div_count = 0, 0, 0, 0, 0
t_div, t_sum, t_mult, t_diff, t_comparison, n, r = 1, 1, 1, 1, 1, 1, 1
Lavg, Tavg = 0, 0


def sum(a, b):
    global sum_count
    sum_count += 1
    return a + b


def mult(a, b):
    global mult_count
    mult_count += 1
    return a * b

def div(a, b):
    global div_count
    div_count += 1
    return a / b


def diff(a, b):
    global diff_count
    diff_count += 1
    return a - b

def compare(a, b, max_or_min):
    global compare_count
    compare_count += 1
    if (max_or_min):
        return max(a, b)
    else:
        return min(a, b)


def check_input(str):
    for i in str:
        if i not in ALFABET:
            return 1
    return 0


def print_matrix(matr, name=''):
    print(name)
    for row in matr:
        string = "   "
        for col in row:
            string += str(col) + "  "
        print(string)


def fill_matrix(m, p, q):
    global A, B, E, G
    A = [[round(random.uniform(-1, 1.001), 3) for _ in range(m)] for i in range(p)]
    B = [[round(random.uniform(-1, 1.001), 3) for _ in range(q)] for i in range(m)]
    E = [[round(random.uniform(-1, 1.001), 3) for _ in range(m)] for i in range(1)]
    G = [[round(random.uniform(-1, 1.001), 3) for _ in range(q)] for i in range(p)]

'''def fill_matrix(m, p, q):
     global A, B, E, G
     A = [[0.594, -0.99],
          [0.948, 0.96]]
     B = [[0.297, -0.069],
          [0.008, -0.801]]
     E = [[0.777, -0.921]]
     G = [[0.149, 0.714],
         [0.868, -0.394]]'''


def find_Tavg():
    Tavg = 0
    Tavg += p * q * m * (3 * (t_diff + t_div) + 7 * t_mult + 3 * t_diff + 2 * t_sum)  # f[i][j][k]
    Tavg += p * q * m * t_mult  # d[i][j][k]
    Tavg += p * q * (m - 1) * t_mult  # /~\k
    Tavg += p * q * ((m + 1) * t_diff + (m - 1) * t_mult)  # \~/k
    Tavg += p * q * (7 * t_mult + 2 * t_sum + 3 * t_diff + t_comparison)  # c[i][j]
    return Tavg


def find_C(x, y, m):
    global C

    def find_compose(a, b):  # min(a,b)
        return compare(a, b, 0)

    def find_tnorm(a, b):  # a * b
        return mult(a, b)

    
    def find_impl(a, b): # sup({ z| ((1-x)*z<=y) /\ (z<=1) })
        difference = diff(1, a) 
        if abs(difference) < 1e-5:  # Если знаменатель дроби близок к нулю 
            difference = 1e-5 if difference > 0 else -1e-5 
        return compare(div(b, difference), 1, 0)
	        

    def find_kf(i, j):
        # f = a_to_b*(2*E[0][k]-1)*E[0][k] + b_to_a*(1+(4*a_to_b-2)*E[0][k])*(1-E[0][k])
        global A, B, E, G, mult_count, diff_count, sum_count, compare_count, n, Tn, p, q, m, Tavg
        multipl_arr = []
        old_Tn = Tn

        for k in range(m):
            a_to_b = find_impl(A[i][k], B[k][j])
            b_to_a = find_impl(B[k][j], A[i][k])
            temp1 = mult(mult(a_to_b, diff(mult(2, E[0][k]), 1)), E[0][k])
            temp2 = mult(mult(b_to_a, sum(1, (mult(diff(mult(4, a_to_b), 2), E[0][k])))), diff(1, E[0][k]))
            # print(f"f00{k}: " + str(temp1 + temp2))
            multipl_arr.append(sum(temp1, temp2))

            Tn += math.ceil(3 / n) * t_diff
            Tn += 1 * t_mult
            Tn += math.ceil(2 / n) * t_div
            Tn += math.ceil(2 / n) * t_comparison
            Tn += 1 * t_mult
            Tn += math.ceil(2 / n) * t_diff
            Tn += math.ceil(2 / n) * t_mult
            Tn += 1 * t_mult
            Tn += 1 * t_sum
            Tn += 1 * t_mult
            Tn += 1 * t_mult
            Tn += 1 * t_sum

        if 6 <= n <= m * 3:
            new_n = n - n % 3  # будет задействоваться максимальное n кратное 3
            count = math.ceil((m * 3) / new_n)  # сколько должно выполниться последовательных операций
            temp = (Tn - old_Tn) / m  # сколько по времени одна итерация
            Tn = Tn - (m - count) * temp  # отнимаем операции, которые можно распараллелить
        elif n >= m * 3:
            temp = (Tn - old_Tn) / m
            Tn = old_Tn + temp

        kf = multipl_arr[0]
        for i_mult in range(1, len(multipl_arr)):
            kf = mult(kf, multipl_arr[i_mult])

        Tn += math.ceil(m - 1) * t_mult

        # print("kf: " + str(kf))
        return kf

    def find_kd(i, j):
        nonlocal m
        global A, B, mult_count, diff_count, sum_count, compare_count, n, Tn, Tavg, q, p
        multipl_arr = []
        old_Tn = Tn

        for k in range(m):
            temp1 = find_tnorm(A[i][k], B[k][j])
            # print(f"d00{k}:" + str(temp1))
            temp2 = diff(1, temp1)
            multipl_arr.append(temp2)
            Tn += 1 * t_mult
            Tn += 1 * t_diff


        if 2 <= n <= m * 1:
            new_n = n - n % 1  # будет задействоваться максимальное n кратное 1
            count = math.ceil((m * 1) / new_n)  # сколько должно выполниться последоватеьных операций
            temp = (Tn - old_Tn) / m  # сколько по времени одна итерация
            Tn = Tn - (m - count) * temp  # отнимаем операции, которые можно распараллелить
        elif n >= m * 1:
            temp = (Tn - old_Tn) / m
            Tn = old_Tn + temp


        dd_res = multipl_arr[0]
        for i_mult in range(1, len(multipl_arr)):
            dd_res = mult(dd_res, multipl_arr[i_mult])
        dd = diff(1, dd_res)
        # print("kd: " + str(dd))

        Tn += math.ceil(m - 1) * t_mult
        Tn += 1 * t_diff

        return dd

    def find_cij(i, j):
        # cij = f*(3*G[i][j] - 2)*G[i][j] + (d+(4*f_and_d-3*d)*G[i][j])*(1-G[i][j])
        global A, B, E, G, sum_count, diff_count, mult_count, compare_count, n, Tn
        d = find_kd(i, j)  # with \~/k
        f = find_kf(i, j)  # with /~\k


        f_and_d = find_compose(f, d)
        # print("f_d: ", f_and_d)
        cij = sum(mult(mult(f, diff(mult(3, G[i][j]), 2)), G[i][j]),
                  mult(sum(d, mult(diff(mult(4, f_and_d), mult(3, d)), G[i][j])), diff(1, G[i][j])))
        Tn += 1 * t_mult
        Tn += math.ceil(3 / n) * t_mult
        Tn += math.ceil(3 / n) * t_diff
        Tn += math.ceil(2 / n) * t_mult
        Tn += 1 * t_mult
        Tn += math.ceil(2 / n) * t_mult
        Tn += 1 * t_sum

        # print(f"C[{i}][{j}] = {cij}\n")
        return cij

    C = [[find_cij(i, j) for j in range(y)] for i in range(x)]


def main():
    global p, q, m, Tn, n
    while (1):
        m = input("m = ")
        p = input("p = ")
        q = input("q = ")
        n = input("n = ")
        # t_sum = int(input("Время операции суммирования: "))
        # t_mult = int(input("Время операции умножения: "))
        # t_diff = int(input("Время операции вычитания: "))
        # t_comparison = int(input("Время операции сравнения: "))
        print("\n")
        if (check_input(m + p + q + n)):
            print("Некорректный ввод")
            continue
        elif int(n) == 0 or int(p) == 0 or int(m) == 0 or int(q) == 0:
            print("Введите значения больше 0")
            continue
        else:
            p = int(p)
            q = int(q)
            m = int(m)
            fill_matrix(m, p, q)
            n = int(n)
            find_C(int(p), int(q), int(m))
            break

    T1 = mult_count * t_mult + diff_count * t_diff + sum_count * t_sum + compare_count * t_comparison + div_count * t_div
    Ky = T1 / Tn
    e = Ky / n
    r = p * q + p * m + q * m + 1 * m + p * q
    Tavg = find_Tavg()
    Lavg = Tavg/r
    D = Tn / Lavg

    print_matrix(A, "\nA:")
    print_matrix(B, "\nB:")
    print_matrix(E, "\nE:")
    print_matrix(G, "\nG:")
    print_matrix(C, "\nC:")

    print("\nParametrs:")
    print("T1 = " + str(T1))
    print("Tn = " + str(Tn))
    print("r = " + str(r))
    print("Ky = " + str(Ky))
    print("e = " + str(e))
    print("Lsum = " + str(Tn))
    print("Lavg = " + str(Lavg))
    print("D = " + str(D))


main()