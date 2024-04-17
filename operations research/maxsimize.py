from scipy.optimize import linprog


c = [-5, -8, -9, -8, -7, -6, -7, -8, -6, -8, -6, -6]

A_eq = [
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
]

b_eq = [21, 27, 38, 14]

A_ub = [
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
]

b_ub = [33, 45, 22]

x_bounds = [(0, None)] * 12

result = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method='highs')

print("Оптимальное решение:")
print(result.x)
print("Оптимальное цена:")
print(-result.fun)
