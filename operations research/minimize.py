from scipy.optimize import linprog

c = [2, 4, 6, 5, 3, 2, 3, 5, 4]

A_eq = [
    [1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1],
]

b_eq = [20, 30, 25]

A_ub = [
    [1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1],
]

b_ub = [25, 25, 35]

x_bounds = [(0, None)] * 9

result = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method='highs')

print("Оптимальное решениеn:")
print(result.x)
print("Оптимальное цена:")
print(result.fun)
