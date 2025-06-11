# Модели решения задач в интеллектуальных системах
# Лабораторная работа 1
# Вариант 3.    
# 221703, Демидовец Д.В.
# Дата: 1.05.2025
# Источники: https://studfile.net/preview/8841236/page:7/

import os

DIGIT = 4
UPPER_LINE = 2**DIGIT - 1
LOWER_LINE = 0
HUGE_TAB = 30
MIDDLE_TAB = 20
TINY_TAB = 6

# перевод десятичного числа в двоичную систему
def to_binary(value):
    value = abs(value)
    result = []
    while value > 0:
        result.insert(0, value % 2)
        value //= 2
    return result

# перевод в двоичную с заполнением до 4го разряда
def to_binary_direct(value):
    result = to_binary(value)
    while len(result) < DIGIT:
        result.insert(0, 0)
    return result


# перевод двоичного числа в десятичную систему
def to_decimal(binary_list):
    result = 0
    for i, bit in enumerate(reversed(binary_list)):
        result += bit * (2**i)
    return result

# сумма бинарных чисел
def summ(x1, x2):
    len_diff = abs(len(x1) - len(x2))
    if len(x1) < len(x2):
        x1 = [0] * len_diff + x1
    elif len(x2) < len(x1):
        x2 = [0] * len_diff + x2

    result = []
    carry = 0
    for i in range(len(x1) - 1, -1, -1):
        bit_sum = x1[i] + x2[i] + carry
        result.insert(0, bit_sum % 2)
        carry = bit_sum // 2
    if carry:
        result.insert(0, carry)
    return result

def print_v(binary_list):
    result = ""
    for i, bit in enumerate(binary_list):
        if (len(binary_list) - i) % 4 == 0 and i != 0:
            result += "."
        result += str(bit)
    return result

def print_list_v(list_of_binary_lists):
    return " ".join(print_v(binary_list) for binary_list in list_of_binary_lists)


# ввод десятичных значений
def input_number(length):
    decimal_list = []
    binary_list = []
    while len(decimal_list) < length:
        try:
            temp = input(f"Введите число {len(decimal_list) + 1}: ")
            num = int(temp)
            if not (LOWER_LINE <= num <= UPPER_LINE):
                raise ValueError(f"Ошибка! Введите число между {LOWER_LINE} и {UPPER_LINE}")
            decimal_list.append(num)
            binary_list.append(to_binary_direct(num))
        except ValueError as e:
            print(e)
            print("Требуется целочисленное число.")
    print("Числа в двоичном преставлении:", print_list_v(binary_list))
    return decimal_list, binary_list

class Conveyer:
    def __init__(self, a_list, b_list):
        if len(a_list) != len(b_list):
            raise ValueError("Длина вектора А и В должны быть равна.")
        self.a_list = a_list
        self.b_list = b_list
        self.digit = DIGIT  
        self.state = []
        self.state_stage = []
        self.inicial_pairs = list(zip(a_list, b_list))
        self.initial_stage = [] 
        self.multipliable = []
        self.multiplier = [] 
        self.part_proizv = []
        self.part_summ = []
        self.result = [] 

    # этап такта конвейера
    def step(self, prev_state):
        multipliable = prev_state[0]
        multiplier = prev_state[1]
        part_proizv = prev_state[2]
        part_summ = prev_state[3]

        multipliable = [0] + multipliable[:-1]
        sign = multiplier[0]
        part_proizv = multipliable if sign else [0] * (DIGIT * 2) 
        part_summ = summ(part_proizv, part_summ)
        multiplier = multiplier[1:] 

        return [multipliable, multiplier, part_proizv, part_summ]

    # такт конвейера
    def tact(self):
        self.state_stage = [[] for _ in range(DIGIT)]

        result_count = 0
        index = 0
        while result_count != len(self.a_list):
            self.init(index)

            for i in range(DIGIT - 1, -1, -1):
                if i == 0:
                    if self.initial_stage:
                        self.state_stage[i] = self.step(self.initial_stage)
                    else:
                        self.state_stage[i] = []
                    continue

                if not self.state_stage[i - 1]:
                    continue

                self.state_stage[i] = self.step(self.state_stage[i - 1])
                self.state_stage[i - 1] = []

                if i == DIGIT - 1 and self.state_stage[i]:
                    result_count += 1

            
            self.output(self.state_stage, index+1)
            print(f"\nТекущий такт {index + 1}")
            input("Нажмите Enter для следующего такта...")
            index += 1

    # подготовка к первому этапу
    def init(self, index):
        if index < len(self.a_list):
            self.state.insert(0, (self.a_list[index], self.b_list[index]))
            self.state = self.state[:DIGIT]
            multipliable = self.a_list[index] + [0] * DIGIT
            multiplier = self.b_list[index]  
            part_proizv = [0] * (DIGIT * 2)
            part_summ = [0] * (DIGIT * 2)
            self.initial_stage = [multipliable, multiplier, part_proizv, part_summ]
        else:
            self.initial_stage = []

    # вывод таблицы
    def output(self, state_stage, clock_cycle):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(len(self.inicial_pairs)):
            print(f"Пара {i+1}: \n DEC: {to_decimal(self.inicial_pairs[i][0])} * {to_decimal(self.inicial_pairs[i][-1])} \n BIN: {self.inicial_pairs[i][0]} * {self.inicial_pairs[i][-1]}")
        print(f"{'Этап':<{HUGE_TAB}}{'Множимое':<{MIDDLE_TAB}} (10)  {'Множитель':<{MIDDLE_TAB}} (10)  {'Частичное произведение':<{MIDDLE_TAB}} (10)  {'Частичная сумма':<{MIDDLE_TAB}} (10)")
        for i, stage in enumerate(state_stage):
            if not stage:
                print(f"{i:<{HUGE_TAB}}{'--------':<{MIDDLE_TAB}} --  {'---------':<{MIDDLE_TAB}}    --  {'----------------------':<{MIDDLE_TAB}}   --    {'---------------':<{MIDDLE_TAB}} --")
                continue

            multipliable, multiplier, part_proizv, part_summ = stage
            multiplier = [int(multipliable == part_proizv)] + multiplier
            while len(multiplier) != DIGIT:
                multiplier.insert(0,0)

            print(f"{i:<{HUGE_TAB}}{print_v(multipliable):<{MIDDLE_TAB}}  {to_decimal(multipliable):<{TINY_TAB}} {print_v(multiplier):<{MIDDLE_TAB}} {to_decimal(multiplier):<{TINY_TAB}}  {print_v(part_proizv):<{MIDDLE_TAB}} {to_decimal(part_proizv):<{TINY_TAB}}  {print_v(part_summ):<{MIDDLE_TAB-1}}{to_decimal(part_summ):<{TINY_TAB}}")

            if i == DIGIT - 1:
                res = to_decimal(part_summ)
                print(f"\Ответ: {res}")
                self.result.append((res, clock_cycle))

    # частичная сумма (итоговое произведение)       
    def get_results(self):
        return self.result

if __name__ == "__main__":
    length = 0
    while length <= 0:
        try:
            input_str = input("\nКоличество пар: ")
            length = int(input_str)
            if length <= 0:
                print("Ошибка! Требуется положительное число.")
        except ValueError:
            print("Ошибка! Требуется целочисленное число")

    a_decimal, a_binary = input_number(length)
    b_decimal, b_binary = input_number(length)

    for i in range(length):
        print(f"{a_decimal[i]} {b_decimal[i]}")

    conveyer = Conveyer(a_binary, b_binary)
    conveyer.tact()
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(len(conveyer.inicial_pairs)):
            print(f"Пара {i+1}: \n DEC: {to_decimal(conveyer.inicial_pairs[i][0])} * {to_decimal(conveyer.inicial_pairs[i][-1])} \n BIN: {conveyer.inicial_pairs[i][0]} * {conveyer.inicial_pairs[i][-1]}")
    for answer, res in conveyer.get_results():
        print(f"Ответ: {answer}, Текущий такт: {res}")
    print(f"Общие количество тактов: {conveyer.get_results()[-1][-1]}")

    