import numpy as np
from scipy.optimize import linprog

# Коэффициенты целевой функции для минимизации
c = [-2, 1, 4, -1, -1]

# Коэффициенты левой части системы уравнений
A = np.array([
    [0, 1, 0, 2, -1],
    [1, 0, 0, -1, -1],
    [0, 2, 1, 0, 2]
])

# Значения правой части системы уравнений
b = [1, 1, 4]

# Ограничения для переменных (x1, x2, x3, x4, x5 >= 0)
x_bounds = [(0, None), (0, None), (0, None), (0, None), (0, None)]

# Решение задачи линейного программирования
result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method="simplex")

# Вывод результатов
print("Результат оптимизации:")
print("Значение целевой функции (минимум):", result.fun)
print("Оптимальные значения переменных:")
for i, x in enumerate(result.x, start=1):
    print(f"x{i} = {x}")
