from dolfin import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Загрузка сетки
mesh = Mesh("group_ellips.xml")  # <-- название файла от GMSH
boundaries = MeshFunction("size_t", mesh, "group_ellips_facet_region.xml")
ds = Measure("ds", subdomain_data=boundaries)

# Функциональное пространство
V = FunctionSpace(mesh, "CG", 1)

# Информация о сетке
print(f"Число ячеек: {mesh.num_cells()}")
print(f"Число узлов: {mesh.num_vertices()}")
print(f"Размерность пространства: {V.dim()}")

# Граничные условия
u_infinity = Expression("x[1]", degree=2)
H = 3
psi_top = u_infinity * H

# Создание граничных условий
bcs = [
    DirichletBC(V, Constant(0.0), boundaries, 101),  # нижняя граница
    DirichletBC(V, psi_top / 3, boundaries, 102),    # верхняя
    DirichletBC(V, psi_top / 3, boundaries, 103),    # левая
    DirichletBC(V, psi_top / 3, boundaries, 104),    # правая
    DirichletBC(V, Constant(1.5), boundaries, 11),    # контуры всех эллипсов
    

    
]

# Вариационная постановка
u = TrialFunction(V)
v = TestFunction(V)
a = dot(grad(u), grad(v)) * dx
L = Constant(0.0) * v * dx

# Решение
u = Function(V)
solve(a == L, u, bcs)

# Вычисление поля скорости
V_vector = VectorFunctionSpace(mesh, "CG", 1)
velocity = project(as_vector((u.dx(1), -u.dx(0))), V_vector)
velocity_magnitude = project(sqrt(dot(velocity, velocity)), V)

# Циркуляция по эллипсам
n = FacetNormal(mesh)
u_n = dot(grad(u), n)
Gamma = assemble(u_n * ds(5))
print(f"Циркуляция по контурам эллипсов: {Gamma:.5e}")

# Визуализация
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

fig, ax = plt.subplots(figsize=(10, 10))
cbar = plt.colorbar(
    plt.tricontourf(x, y, triangles, velocity_values, levels=100, cmap='viridis')
)
cbar.set_label("Модуль скорости")

# Автоматическая отрисовка эллипсов
additional_centers = [
    (0.5, 0.5), (1.5, 0.5), (0.5, 2.5),
    (0.5, 1.5), (1.5, 1.5), (1.5, 2.5),
    (2.5, 0.5), (2.5, 1.5), (2.5, 2.5)
]
a, b = 0.275, 0.125
alpha = np.pi / 4
theta = np.linspace(0, 2 * np.pi, 200)

# Построение дополнительных эллипсов
for cx, cy in additional_centers:
    x_ellipse = a * np.cos(theta)
    y_ellipse = b * np.sin(theta)
    x_rot = cx + x_ellipse * np.cos(alpha) - y_ellipse * np.sin(alpha)
    y_rot = cy + x_ellipse * np.sin(alpha) + y_ellipse * np.cos(alpha)
    ax.fill(x_rot, y_rot, 'w', zorder=3)
    ax.plot(x_rot, y_rot, 'r', linewidth=1, zorder=4)

ax.scatter(critical_x, critical_y, color='lime', s=50, label="Критические точки", zorder=5)

levels = np.linspace(0, 3.0, 45)
levels = np.append(levels, 0.5)
levels = np.append(levels, 1.5)    
levels = np.append(levels, 2.5)        # добавляем вручную уровень 0.5
levels = np.unique(np.round(levels, 8))    # удаляем дубликаты и сортируем
isolines = plt.tricontour(x, y, triangles, u_values, levels=levels, colors='black', linewidths=1.2)

# Подписи линий тока
ax.clabel(isolines, inline=True, fontsize=10, fmt="%.2f")

# Легенда
legend_elements = [
    Line2D([0], [0], color='r', linewidth=1.5, label="Контуры эллипсов"),
    Line2D([0], [0], color='black', linestyle='-', label="Линии тока"),
    plt.Line2D([], [], color='lime', marker='o', linestyle='None', markersize=10, label="Критические точки")
]

ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Настройки графика
ax.set_xlim(0, 3)
ax.set_ylim(0, 3)
ax.set_aspect('equal')
plt.xlabel("L")
plt.ylabel("H")
plt.title("Обтекание массива эллипсов")
plt.tight_layout()
plt.savefig("ellips_array_result.png", dpi=1000)
plt.show()
