import numpy as np
import matplotlib.pyplot as plt


np.random.seed(42)
k_true = 2.5  # Справжній нахил
b_true = -1.0  # Справжній перехват
n_points = 100

x = np.random.uniform(-10, 10, n_points)
y = k_true * x + b_true + np.random.normal(scale=5.0, size=n_points)

#метод найменших квадратів
def least_squares_fit(x, y):
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xx = np.sum(x * x)
    sum_xy = np.sum(x * y)
    
    denominator = n * sum_xx - sum_x * sum_x
    k = (n * sum_xy - sum_x * sum_y) / denominator
    b = (sum_y * sum_xx - sum_x * sum_xy) / denominator
    
    return k, b

k_fit, b_fit = least_squares_fit(x, y)

k_poly, b_poly = np.polyfit(x, y, 1)

plt.figure(figsize=(10, 6))
plt.scatter(x, y, label='Згенеровані дані', color='blue', alpha=0.5)
plt.plot(x, k_true * x + b_true, label='Справжня пряма', color='green', linestyle='dotted', linewidth=2)
plt.plot(x, k_fit * x + b_fit, label='Метод найменших квадратів', color='red', linestyle='solid', linewidth=2)
plt.plot(x, k_poly * x + b_poly, label='np.polyfit', color='orange', linestyle='dashed', linewidth=2)

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Порівняння методів регресії')
plt.grid(True)
plt.show()

print(f"Справжні параметри: k = {k_true}, b = {b_true}")
print(f"Метод найменших квадратів: k = {k_fit:.4f}, b = {b_fit:.4f}")
print(f"np.polyfit: k = {k_poly:.4f}, b = {b_poly:.4f}")
