from dolfin import *
import meshio
import matplotlib.pyplot as plt
import numpy as np

# Загрузка сетки из файла .msh с использованием meshio
msh_file = "group_ellips.msh"
mesh_data = meshio.read(msh_file)

# Извлечение информации о сетке
points = mesh_data.points[:, :2]  # Точки (только x, y)
cells = mesh_data.cells_dict["triangle"]  # Треугольные элементы

# Создание сетки в FEniCS
mesh = Mesh()
editor = MeshEditor()
editor.open(mesh, "triangle", 2, 2)  # 2D треугольная сетка
editor.init_vertices(len(points))
editor.init_cells(len(cells))

# Добавление точек и ячеек
for i, point in enumerate(points):
    editor.add_vertex(i, point)
for i, cell in enumerate(cells):
    editor.add_cell(i, cell)

editor.close()

# Получение числа узлов и треугольников
n_v = mesh.num_vertices()   # Число узлов
n_c = mesh.num_cells()      # Число треугольников

# Вывод информации
print(f"Число узлов сетки: {n_v}")
print(f"Число треугольников: {n_c}")

# Визуализация сетки 
plt.figure()
plot(mesh)
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.savefig('group_ellips_2.png', format="png", dpi=600)
plt.show()
