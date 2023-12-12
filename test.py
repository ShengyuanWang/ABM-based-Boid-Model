from scipy.optimize import linprog
obj = [-1,-1]
lhs_ineq = [[ 2,  1],[2, 4]]
rhs_ineq = [29, 50]
x0_bounds = (2, None)
x1_bounds = (5, None)
res = linprog(obj, A_ub=lhs_ineq, b_ub=rhs_ineq, bounds=[x0_bounds, x1_bounds], method='highs')
max_fish = -res.fun
gouramis, danios = res.x
print(f"Maximum number of fish that can be kept is: {max_fish:.2f}")
print(f"Number of gouramis: {gouramis:.2f}")
print(f"Number of danios: {danios:.2f}")