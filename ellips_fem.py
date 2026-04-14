import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from dolfin import *

# Загрузка сетки
mesh = Mesh("ellips_1.xml")
boundaries = MeshFunction("size_t", mesh, "ellips_facet_region_1.xml")
ds = Measure("ds", subdomain_data=boundaries)

# Определение функционального пространства
V = FunctionSpace(mesh, "CG", 2)

# Информации о сетке и числе искомых величин
n_c = mesh.num_cells()
n_v = mesh.num_vertices()
n_d = V.dim()

print(f"Число ячеек сетки: {n_c}")
print(f"Число узлов сетки: {n_v}")
print(f"Число искомых дискретных значений: {n_d}")

# Условие на входе в канал
u_infinity = Expression("x[1]", degree=2)
H = 1
psi_0 = u_infinity * H

# Граничные условия
bcs = [DirichletBC(V, Constant(0.0), boundaries, 1), 
       DirichletBC(V, u_infinity * H, boundaries, 2),
       DirichletBC(V, Constant(0.5), boundaries, 5),
       DirichletBC(V, u_infinity * H, boundaries, 3),
       DirichletBC(V, u_infinity * H, boundaries, 4)]

# Вариационная задача
u = TrialFunction(V)
v = TestFunction(V)
f = Constant(0.0)
a = dot(grad(u), grad(v)) * dx
L = f * v * dx

# Решение задачи
u = Function(V)
solve(a == L, u, bcs)

# Вычисление скорости
V_vector = VectorFunctionSpace(mesh, "CG", 2)
velocity = project(as_vector((u.dx(1), -u.dx(0))), V_vector)
velocity_magnitude = project(sqrt(dot(velocity, velocity)), V)

# Вычисление циркуляции
n = FacetNormal(mesh)
u_n = dot(grad(u), n)
Gamma = assemble(u_n * ds(subdomain_data=boundaries, subdomain_id=5))
print(f"Циркуляция: {Gamma:.5e}")

# Сетка для визуализации
coordinates = mesh.coordinates()
x = coordinates[:, 0]
y = coordinates[:, 1]
triangles = mesh.cells()
u_values = u.compute_vertex_values(mesh)
velocity_values = velocity_magnitude.compute_vertex_values(mesh)

# Поиск критических точек (где скорость почти нулевая)
threshold = 1e-1
critical_points = (velocity_values < threshold)
critical_x = x[critical_points]
critical_y = y[critical_points]

# График
fig, ax = plt.subplots(figsize=(10, 10))
cbar = plt.colorbar(plt.tricontourf(x, y, triangles, velocity_values, levels=100, cmap='viridis'))
cbar.set_label("Модуль вектора скорости")

# Параметры эллипса
cx, cy = 0.5, 0.5  # Центр эллипса
a, b = 0.125, 0.125   # Полуоси эллипса
alpha = np.radians(45)  # Угол поворота

# Генерация эллипса
theta = np.linspace(0, 2 * np.pi, 300)
x_ellipse = a * np.cos(theta)
y_ellipse = b * np.sin(theta)

# Поворот эллипса
ellipse_x = cx + x_ellipse * np.cos(alpha) - y_ellipse * np.sin(alpha)
ellipse_y = cy + x_ellipse * np.sin(alpha) + y_ellipse * np.cos(alpha)

# Отрисовка эллипса
ax.fill(ellipse_x, ellipse_y, 'w', zorder=3)
ellipse_line, = ax.plot(ellipse_x, ellipse_y, 'r', linewidth=2.2, zorder=4)

# Отображение критических точек
ax.scatter(critical_x, critical_y, color='lime', s=100, label="Критические точки", zorder=5)

levels = np.linspace(0, 1.0, 40)
levels = np.append(levels, 0.5)            # добавляем вручную уровень 0.5
levels = np.unique(np.round(levels, 8))    # удаляем дубликаты и сортируем
isolines = plt.tricontour(x, y, triangles, u_values, levels=levels, colors='black', linewidths=1.2)

# Подписи линий тока
ax.clabel(isolines, inline=True, fontsize=10, fmt="%.2f")

# Легенда
legend_elements = [
    Line2D([0], [0], color='r', linewidth=2.2, label="Контур эллипса"),
    Line2D([0], [0], color='black', linestyle='-', label="Линии тока"),
    plt.Line2D([], [], color='lime', marker='o', linestyle='None', markersize=10, label="Критические точки")
]

ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Настройки графика
#plt.tight_layout()  # Оптимизация отступов
plt.savefig('test.png', format="png", dpi=1000)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal', adjustable='box')  # Сохранение пропорций
plt.xlabel("L")
plt.ylabel("H")
plt.title("Обтекание эллипса с циркулляцией")
plt.show()
