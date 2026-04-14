from dolfin import *
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np

# --- Параметры геометрии ---
L = 1.0  # период по x
H = 1.0  # период по y
u_infinity = 1.0
psi_0 = u_infinity * H  # Расход через ячейку

# --- Периодические граничные условия по x и y ---
class PeriodicDomain(SubDomain):
    def inside(self, x, on_boundary):
        return (near(x[0], 0.0) or near(x[1], 0.0)) and on_boundary

    def map(self, x, y):
        if near(x[0], L) and near(x[1], H):
            y[0] = x[0] - L
            y[1] = x[1] - H
        elif near(x[0], L):
            y[0] = x[0] - L
            y[1] = x[1]
        elif near(x[1], H):
            y[0] = x[0]
            y[1] = x[1] - H
        else:
            y[0] = x[0]
            y[1] = x[1]

# --- Загрузка сетки ---
mesh = Mesh("ellips_0275.xml")
boundaries = MeshFunction("size_t", mesh, "ellips_0275_facet_region.xml")
ds = Measure("ds", subdomain_data=boundaries)

# --- Пространство функций с периодичностью ---
V = FunctionSpace(mesh, "CG", 2, constrained_domain=PeriodicDomain())

# --- Граничное условие на контуре эллипса (ψ = 0) ---
bcs = [DirichletBC(V, Constant(0.0), boundaries, 5)]  # ID 5 — кривая цилиндра

# --- Задаем линейную функцию для ψ на поперечной границе: прирост на ψ0 ---
psi_shift = Expression("x[1]*q", q=u_infinity, degree=1)

# --- Вариационная задача ---
u = TrialFunction(V)
v = TestFunction(V)
a = dot(grad(u), grad(v)) * dx
L = Constant(0.0) * v * dx

# --- Решение задачи ---
ψ = Function(V)
solve(a == L, ψ, bcs)

# --- Проекция скорости: u = (∂ψ/∂y, -∂ψ/∂x) ---
Vv = VectorFunctionSpace(mesh, "CG", 2)
velocity = project(as_vector((ψ.dx(1), -ψ.dx(0))), Vv)
velocity_magnitude = project(sqrt(dot(velocity, velocity)), V)

# --- Вычисление циркуляции по границе эллипса ---
n = FacetNormal(mesh)
Gamma = assemble(dot(grad(ψ), n) * ds(5))
print(f"Циркуляция по границе эллипса: {Gamma:.5e}")

# --- Визуализация ---
coords = mesh.coordinates()
cells = mesh.cells()
triang = tri.Triangulation(coords[:, 0], coords[:, 1], cells)

# --- Функция тока ---
plt.figure(figsize=(6, 5))
ψ_vals = ψ.compute_vertex_values(mesh)
plt.tricontourf(triang, ψ_vals, 100, cmap='RdBu_r')
plt.colorbar(label="Функция тока ψ")
plt.title("Функция тока")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')

# --- Поле скорости ---
v_vals = velocity.compute_vertex_values(mesh).reshape((2, -1))
plt.figure(figsize=(6, 5))
plt.quiver(coords[:, 0], coords[:, 1], v_vals[0], v_vals[1], scale=20)
plt.title("Поле скорости")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')

# --- Модуль скорости ---
v_mag_vals = velocity_magnitude.compute_vertex_values(mesh)
plt.figure(figsize=(6, 5))
plt.tricontourf(triang, v_mag_vals, 100, cmap='viridis')
plt.colorbar(label="|v|")
plt.title("Модуль скорости")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')

plt.tight_layout()
plt.show()
