import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root
from matplotlib import transforms
import matplotlib.lines as mlines 


def rotate_coords(x, y, angle_rad):
    """Функция для поворота координат на угол angle_rad (в радианах)"""
    x_rot = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    y_rot = x * np.sin(angle_rad) + y * np.cos(angle_rad)
    return x_rot, y_rot

def ellipse(a, b, alpha, vinf, size):
    vinff = vinf
    b1 = b 
    r = a + b1
    c = np.sqrt(a**2 - b1**2)
    alpha1 = alpha
    
    def t(z):
        return z + np.sqrt(z - c) * np.sqrt(z + c)
    
    def w(z, Gamma):
        return (vinff / 2 * (np.exp(-1j * alpha1) * t(z) + (np.exp(1j * alpha1) * r**2) / t(z)) +
                (Gamma * np.log(t(z))) / (2 * np.pi * 1j))
    
    def w_prime(z, Gamma):
        h = 1e-8
        return (w(z + h, Gamma) - w(z - h, Gamma)) / (2 * h)
    
    Gamma = 0.00000001 # Задаем не нулевую так как функция чувствительная к начальному приближению
    
    # Построение эллипса
    theta = np.linspace(0, 2*np.pi, 100000)
    x_ellipse = a * np.cos(theta)
    y_ellipse = b1 * np.sin(theta)
    
    dz = (x_ellipse[1:] - x_ellipse[:-1]) + 1j * (y_ellipse[1:] - y_ellipse[:-1])
    velocity = w_prime(x_ellipse[:-1] + 1j * y_ellipse[:-1], Gamma)
    circulation = np.sum(velocity * dz)
    print(f"Циркуляция по контуру эллипса: {circulation.real:.5f}")
    
    # Генерация сетки для потока (большая область 3x3)
    x = np.linspace(-1.5, 1.5, size)  # Изменили диапазон на -1 до 1 (для области 3x3)
    y = np.linspace(-1.5, 1.5, size)  # Изменили диапазон на -1 до 1 (для области 3x3)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    U = np.conjugate(w_prime(Z, Gamma))
    Ux = np.real(U)
    Uy = np.imag(U)
    
    # Маска эллипса
    mask = X**2 / a**2 + Y**2 / b1**2 >= 1
    Ux = np.ma.masked_where(~mask, Ux)
    Uy = np.ma.masked_where(~mask, Uy)
    
    def find_stagnation_point(initial_guess):
        def func(z_real_imag):
            z_complex = z_real_imag[0] + 1j * z_real_imag[1]
            w_p = w_prime(z_complex, Gamma)
            return [np.real(w_p), np.imag(w_p)]
        
        sol = root(func, [np.real(initial_guess), np.imag(initial_guess)], method='hybr')
        
        z_stag = sol.x[0] + 1j * sol.x[1]
        if (np.real(z_stag) ** 2 / a ** 2 + np.imag(z_stag) ** 2 / b1 ** 2) < 1:
            return z_stag
        return None
    
    stagnation_point1 = find_stagnation_point(a+ 0.275)
    stagnation_point2 = find_stagnation_point(-a - 0.175)
    
    stagnation_points = [p for p in [stagnation_point1, stagnation_point2] if p is not None]
    
    # Проверка на наличие точек стагнации
    if len(stagnation_points) == 0:
        print("Не удалось найти точки стагнации.")
    else:
        # Отображение
        fig, ax = plt.subplots(figsize=(size/100, size/100))

        Ux = np.ma.masked_invalid(Ux)
        Uy = np.ma.masked_invalid(Uy)

        # Вычисление скорости
        speed = np.sqrt(np.abs(Ux)**2 + np.abs(Uy)**2)

        # Цветовая подложка
        c = ax.pcolormesh(X + np.sqrt(2) / 2, Y, speed, shading='auto', cmap='viridis') 

        # Добавляем цветовую шкалу
        plt.colorbar(c, label='Модуль вектора скорости')

        # Стримплот
        #stream = ax.streamplot(X + np.sqrt(2) / 2, Y, Ux, Uy, density=4, minlength=0.8, color='black', linewidth=1.2, arrowsize=0)
        start_points = [
            [0.0, 0.0], [0.025, 0.025], [0.05, 0.05], [0.075, 0.075], [0.1, 0.1], [0.125, 0.125], [0.15, 0.15],
            [0.175, 0.175], [0.2, 0.2], [0.225, 0.225], [0.25, 0.25], [0.275, 0.275], [0.3, 0.3], [0.341, 0.341],  [0.354269, 0.354269],
             [0.375, 0.375], [0.4, 0.4], [0.425, 0.425], [0.45, 0.45], [0.475, 0.475], [0.5, 0.5], 
            [0.525, 0.525], [0.55, 0.55], [0.575, 0.575], [0.6, 0.6], [0.625, 0.625], [0.65, 0.65], [0.675, 0.675],
            [0.7, 0.7], [0.725, 0.725], [0.75, 0.75], [0.775, 0.775], [0.8, 0.8], [0.825, 0.825], [0.85, 0.85],
            [0.875, 0.875], [0.9, 0.9], [0.925, 0.925], [0.95, 0.95], [0.975, 0.975], [1.0, 1.0]
        ]
        for point in start_points:
            ax.streamplot(X + np.sqrt(2) / 2, Y, Ux, Uy, start_points=[point], color='black', linewidth=1, density=4, arrowsize=0)


        

        # Поворот всех элементов на 45 градусов
        angle = 45  # Угол поворота в градусах
        rotation = transforms.Affine2D().rotate_deg(angle)

        # Применяем поворот ко всем элементам
        ax.set_aspect('equal', adjustable='box')

        # Ограничиваем область отображения после поворота
        ax.set_xlim(0, 1)  # Ограничиваем отображаемую область 1x1
        ax.set_ylim(0, 1)  # Ограничиваем отображаемую область 1x1

        for collection in ax.collections:
            collection.set_transform(rotation + ax.transData)
        for line in ax.get_lines():
            line.set_transform(rotation + ax.transData)

        # Поворот эллипса и точек стагнации
        x_ellipse_rot, y_ellipse_rot = rotate_coords(x_ellipse, y_ellipse, np.radians(angle))
        cylinder_line, = ax.plot(x_ellipse_rot + 0.5, y_ellipse_rot + 0.5, 'r', linewidth=2.2, label="Контур цилиндра")

        stagnation_points_rot = [rotate_coords(np.real(p), np.imag(p), np.radians(angle)) for p in stagnation_points]
        stagnation_plot = []
        for i, p in enumerate(stagnation_points_rot):
            x_rot, y_rot = p  # безопасно распаковываем кортеж
            x_plot, y_plot = x_rot + 0.5, y_rot + 0.5
            stagnation_plot.append(ax.scatter(x_plot, y_plot, color='lime', s=100, zorder=3, label="Критические точки"))
            print(f"Критическая точка #{i+1}: x = {x_plot:.5f}, y = {y_plot:.5f}")

        # Создаем прокси для линий тока
        stream_line_proxy = mlines.Line2D([], [], color='black', linewidth=1.2, label="Линии тока")

        # Настройка осей
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        plt.xlabel("L")
        plt.ylabel("H")
        plt.title("Обтекание цилиндра с циркуляцией")

        # Добавляем легенду
        ax.legend(handles=[stagnation_plot[0], cylinder_line, stream_line_proxy], 
                  labels=["Критические точки", "Контур цилиндра", "Линии тока"], loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)

        plt.show()

ellipse(0.225, 0.125, -45/180*np.pi, 1.0, 1000)
