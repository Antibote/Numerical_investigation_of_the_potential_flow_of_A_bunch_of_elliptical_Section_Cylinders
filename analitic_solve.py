import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.integrate import solve_ivp
from matplotlib.lines import Line2D

def circulation_cylinder(a, alpha, vinf, gamma, size):
    # Центр цилиндра
    cx, cy = 0.5, 0.5  
    c = a  # Радиус цилиндра
    alpha_rad = np.radians(alpha)  # Угол атаки в радианах

    def complex_potential(z):
        # Комплексный потенциал с циркуляцией
        return (vinf * (z * np.exp(-1j * alpha_rad) + c**2 / z * np.exp(1j * alpha_rad)) +
                1j * gamma / (2 * np.pi) * np.log(z))

    
    def velocity_field(x, y):
        z = (x - cx) + 1j * (y - cy)
        if np.abs(z) < c:
            return np.nan, np.nan
        # Производная комплексного потенциала — скорость
        w_prime = vinf * (np.exp(-1j * alpha_rad) - c**2 / z**2 * np.exp(1j * alpha_rad)) + \
                  1j * gamma / (2 * np.pi * z)
        return np.real(w_prime), -np.imag(w_prime)
    
    def stagnation_eq(x):
        x = x[0]
        z = complex(x - cx, 0)
        w_prime = vinf * (np.exp(-1j * alpha_rad) - c**2 / z**2 * np.exp(1j * alpha_rad)) + \
                  1j * gamma / (2 * np.pi * z)
        return np.real(w_prime)

    stagnation_x1 = fsolve(stagnation_eq, cx + c)[0]
    stagnation_x2 = fsolve(stagnation_eq, cx - c)[0]
    stagnation_points = np.array([[stagnation_x1, cy], [stagnation_x2, cy]])
    
    # Вычисление циркуляции в стагнационных точках
    def circulation_at_stagnation(x, y):
        z = complex(x - cx, y - cy)
        w_prime = vinf * (np.exp(-1j * alpha_rad) - c**2 / z**2 * np.exp(1j * alpha_rad)) + 1j * gamma / (2 * np.pi * z)
        return np.imag(w_prime)  # Функция тока в стагнационной точке

    # Суммарная циркуляция по двум стагнационным точкам
    total_circulation = 0
    for point in stagnation_points:
        circulation_value = circulation_at_stagnation(point[0], point[1])
        total_circulation += circulation_value
    
    # Вывод стагнационных точек
    for i, point in enumerate(stagnation_points):
        print(f"Критическая точка {i+1}: X = {point[0]}, Y = {point[1]}")
    
    # Вывод суммарной циркуляции
    print(f"Циркуляция: {total_circulation}")
    
    # Создание сетки
    x = np.linspace(0, 1, size)
    y = np.linspace(0, 1, size)
    X, Y = np.meshgrid(x, y)
    
    # Вычисление поля скоростей
    U, V = np.vectorize(velocity_field)(X, Y)

    # Заменяем NaN и Inf на нули
    U = np.nan_to_num(U)
    V = np.nan_to_num(V)
    
    # Вычисление скорости
    speed = np.sqrt(U**2 + V**2)
    
    # График
    fig, ax = plt.subplots(figsize=(10, 10))

    # Линии уровня (контуры)
    contour = ax.contourf(X, Y, speed, levels=np.linspace(np.min(speed), np.max(speed), 1000), cmap='viridis')
    
    # Добавляем цветовую шкалу
    plt.colorbar(contour, label='Модуль вектора скорости')
    
    # Отрисовка цилиндра
    theta = np.linspace(0, 2 * np.pi, 300)
    cylinder_x = cx + c * np.cos(theta)
    cylinder_y = cy + c * np.sin(theta)
    ax.fill(cylinder_x, cylinder_y, 'w', zorder=3)
    cylinder_line, = ax.plot(cylinder_x, cylinder_y, 'r', linewidth=2.2, zorder=4)
    
    # Отметка стагнационных точек
    stagnation_plot = ax.scatter(stagnation_points[:, 0], stagnation_points[:, 1], color='lime', s=100, zorder=5)

    start_points = [
    [0.0, 0.0], [0.025, 0.025], [0.05, 0.05], [0.075, 0.075], [0.1, 0.1], [0.125, 0.125], [0.15, 0.15], [0.175, 0.175], 
    [0.2, 0.2], [0.225, 0.225], [0.25, 0.25], [0.275, 0.275], [0.3, 0.3], [0.325, 0.325], 
    [0.35, 0.35], [0.375, 0.375], [0.4, 0.4], [0.425, 0.425], [0.45, 0.45], [0.475, 0.475],  
    [0.5, 0.5], [0.525, 0.525], [0.55, 0.55], [0.575, 0.575], [0.6, 0.6], [0.625, 0.625], 
    [0.65, 0.65], [0.675, 0.675], [0.7, 0.7], [0.725, 0.725], [0.75, 0.75], [0.775, 0.775], 
    [0.8, 0.8], [0.825, 0.825], [0.85, 0.85], [0.875, 0.875], [0.9, 0.9], [0.925, 0.925], 
    [0.95, 0.95], [0.975, 0.975], [1.0, 1.0]
    ]
    for point in start_points:
        ax.streamplot(X, Y, U, V, start_points=[point], color='black', linewidth=1, density =4, arrowsize=0)
    
    # Линии тока вокруг цилиндра
    num_points = 3  # Число точек для линий тока вокруг цилиндра
    theta_stream = np.linspace(0, 2 * np.pi, num_points)
    stream_start_points = np.array([cx + c * np.cos(theta_stream), cy + c * np.sin(theta_stream)]).T

    stream_plot = ax.streamplot(X, Y, U, V, start_points=stream_start_points, color='black', linewidth=1, density=10, arrowsize=0)

    # Настройка осей
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    plt.xlabel("L")
    plt.ylabel("H")
    plt.title("Обтекание цилиндра с циркулляцией")
    
    # Добавляем легенду
    ax.legend(handles=[stagnation_plot, cylinder_line, Line2D([0], [0], color='black', lw=1)],
              labels=["Критические точки", "Контур цилиндра", "Линии тока"], loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)

    # Сохраняем изображение в файл PNG
    plt.savefig("circulation_cylinder.png", format="png")
    plt.close(fig)  # Закрываем фигуру

# Вызов функции
circulation_cylinder(0.125, 0, 1.0, 0.0, 1500)  # Увеличьте размер сетки
