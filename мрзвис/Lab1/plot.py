import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

n1 = 1   
n2 = 4 

r_values = np.arange(1, 31) 

K_values_1 = (r_values * n1) / (n1 + r_values - 1) 
K_values_4 = (r_values * n2) / (n2 + r_values - 1) 

E_values_1 = K_values_1 / n1
E_values_4 = K_values_4 / n2

plt.figure(figsize=(12, 7))
plt.plot(r_values, K_values_1, 'r--s', linewidth=2, markersize=8, label='1-этапный конвейер')
plt.plot(r_values, K_values_4, 'b-o', linewidth=2, markersize=8, label='4-этапный конвейер')

plt.title('Сравнение коэффициента ускорения $K_У$ для конвейеров', fontsize=14)
plt.xlabel('Ранг задачи $r$', fontsize=12)
plt.ylabel('$K_У = \\frac{T_1}{T_n}$', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(r_values)
plt.legend()
plt.ylim(0, 6.5)  

plt.axhline(y=6, color='gray', linestyle='dashed', linewidth=1)
plt.text(x=1, y=6.1, s='Теоретический предел для 4-этапного конвейера', fontsize=10)

plt.show()

plt.figure(figsize=(12, 7))
plt.plot(r_values, E_values_1, 'r--s', linewidth=2, markersize=8, label='1-этапный конвейер')
plt.plot(r_values, E_values_4, 'g-D', linewidth=2, markersize=8, label='4-этапный конвейер')

plt.title('График зависимости эффективности $e$ от ранга задачи $r$', fontsize=14)
plt.xlabel('Ранг задачи $r$', fontsize=12)
plt.ylabel('Эффективность $e$', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(r_values)
plt.legend()
plt.ylim(0, 1.1)  

plt.show()

def T1(n, r):
  if n <= 0 or r <= 0:
      return 0
  return n * r

def Tn(n, r):
  if n <= 0 or r <= 0:
      return 0
  return n + r - 1

def Ky(n, r):
  t1 = T1(n, r)
  tn = Tn(n, r)
  if tn == 0:
    return np.nan
  return t1 / tn

def e(n, r):
  ky = Ky(n, r)
  if n == 0:
      return np.nan
  return ky / n

N_MAX = 4 
R_MAX = 4 

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial']

n_values_plot3 = np.arange(1, N_MAX + 1) 

r_fixed_values = np.arange(1, R_MAX + 1) 
plt.figure(figsize=(8, 6))

for r_fix in r_fixed_values:
  ky_values = [Ky(n_val, r_fix) for n_val in n_values_plot3 if n_val in (1, 4)]  # только n = 1 и 4
  n_filtered = [n_val for n_val in n_values_plot3 if n_val in (1, 4)]
  plt.plot(n_filtered, ky_values, marker='o', linestyle='None', label=f'r={r_fix}')  # только точки

plt.title(f'График зависимости коэффициента ускорения $K_y$ от кол-ва этапов $n$ (для r=1..{R_MAX})')
plt.xlabel('Кол-во этапов, $n$')
plt.ylabel('Коэффициент ускорения, $K_y$')
plt.xticks(n_values_plot3)
plt.ylim(bottom=0) 
plt.grid(True)
plt.legend()
plt.show()


plt.figure(figsize=(8, 6))

for r_fix in r_fixed_values:
  e_values_filtered = [e(n_val, r_fix) for n_val in n_values_plot3 if n_val in (1, 4)]
  n_filtered = [n_val for n_val in n_values_plot3 if n_val in (1, 4)]
  plt.plot(n_filtered, e_values_filtered, marker='o', linestyle='None', label=f'r={r_fix}')  # только точки

plt.title(f'График зависимости эффективности $e$ от кол-ва этапов $n$ (для r=1..{R_MAX})')
plt.xlabel('Кол-во этапов, $n$')
plt.ylabel('Эффективность, $e$')
plt.xticks(n_values_plot3)
plt.ylim(0, 1.1) 
plt.grid(True)
plt.legend()
plt.show()


''' Графики с линиями
plt.figure(figsize=(8, 6))

for r_fix in r_fixed_values:
  ky_values = [Ky(n_val, r_fix) for n_val in n_values_plot3]
  plt.plot(n_values_plot3, ky_values, marker='o', linestyle='-', label=f'r={r_fix}')

plt.title(f'График зависимости коэффициента ускорения $K_y$ от кол-ва этапов $n$ (для r=1..{R_MAX})')
plt.xlabel('Кол-во этапов, $n$')
plt.ylabel('Коэффициент ускорения, $K_y$')
plt.xticks(n_values_plot3)
plt.ylim(bottom=0) 
plt.grid(True)
plt.legend()
plt.show()


plt.figure(figsize=(8, 6))

for r_fix in r_fixed_values:
  e_values = [e(n_val, r_fix) for n_val in n_values_plot3]
  plt.plot(n_values_plot3, e_values, marker='o', linestyle='-', label=f'r={r_fix}')

plt.title(f'График зависимости эффективности $e$ от кол-ва этапов $n$ (для r=1..{R_MAX})')
plt.xlabel('Кол-во этапов, $n$')
plt.ylabel('Эффективность, $e$')
plt.xticks(n_values_plot3)
plt.ylim(0, 1.1) 
plt.grid(True)
plt.legend()
plt.show() '''