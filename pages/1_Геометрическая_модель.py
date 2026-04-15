import streamlit as st
import base64
import subprocess
import os
import math
import gmsh
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

def run_gmsh(file_path):
    try:
        env = os.environ.copy()
        env["LIBGL_ALWAYS_SOFTWARE"] = "1"  # Используем программный рендеринг
        subprocess.run(["gmsh", file_path], check=True, env=env)
        st.success("Gmsh успешно запущен в программном режиме!")
    except FileNotFoundError:
        st.error("Gmsh не найден. Убедитесь, что он установлен и доступен в PATH.")
    except subprocess.CalledProcessError:
        st.error("Ошибка при запуске Gmsh.")

def show_code(code, language="python"):
    st.code(code, language)


##### Геометрическая модель
st.markdown(r"""
**Схема течения**
""")

# Загрузка изображения
st.image("6.png", 
        use_container_width=True)

st.markdown(r"""
**Ячейка периодичности**
""")
st.image("7.png", 
        use_container_width=True)

st.markdown(r"""
+ $D -$ эллиптическое сечение цилиндров, повернутых на 45 градусов  
+ $\gamma -$ граница цилиндра  
+ $r, \ R -$ малая и большая полуоси эллипса    
+ $(l, h)-$ центр цилиндра  
+ $\Omega -$ расчетная область  
+ $L, H -$ длина и ширина периодической ячейки  
+ $\Gamma -$ граница ячейки периодичности
""")
r"""
##### Файл геометрии
"""
with st.expander("Параметры ячейки периодичности"):
    code_1 = """
    // Параметры прямоугольника
    L = 1;      // Ширина прямоугольника
    H = 1;      // Высота прямоугольника
    """
    show_code(code_1, "python")
with st.expander("Параметры цилиндра"):
    code_2 = """
    // Параметры кругового выреза
    r = 0.125;  // Малый радиус эллипса
    R = 0.125; // Большой радиус эллипса
    l = L/2;   // X-координата центра эллипса
    h = H/2;   // Y-координата центра эллипса
    """
    show_code(code_2, "python")
with st.expander("Параметризация расчетной области"):
    code_3 = """
    // Размеры сетки
    N = 30;     // Количество точек на границе
    d = H/N;    // Размер сетки по ширине канала
    dd = 0.025*d; // Размер сетки на окружности
    """
    show_code(code_3, "python")
with st.expander("Точки ячейки периодичности"):
    code_4 = """
    // Точки для прямоугольника
    Point(1) = {0, 0, 0, d};
    Point(2) = {L, 0, 0, d};
    Point(3) = {L, H, 0, d};
    Point(4) = {0, H, 0, d};
    """
    show_code(code_4, "python")
with st.expander("Построение границ ячейки периодичности"):
    code_5 = """
    // Линии для прямоугольника
    Line(1) = {1, 2};  // Нижняя граница
    Line(2) = {2, 3};  // Правая граница
    Line(3) = {3, 4};  // Верхняя граница
    Line(4) = {4, 1};  // Левая граница
    """
    show_code(code_5, "python")
with st.expander("Точки цилиндра"):
    code_6 = """
    // Точки для эллипса
    Point(5) = {l, h, 0, dd};
    Point(6) = {l + r, h, 0, dd};
    Point(7) = {l, h + R, 0, dd};
    Point(8) = {l - R, h, 0, dd};
    Point(9) = {l, h - r, 0, dd};
    """
    show_code(code_6, "python")
with st.expander("Построение дуг цилиндра"):
    code_7 = """
    // Дуги для эллипса
    Ellipse(5) = {6, 5, 7};
    Ellipse(6) = {7, 5, 8};
    Ellipse(7) = {8, 5, 9};
    Ellipse(8) = {9, 5, 6};
    """
    show_code(code_7, "python")
with st.expander("Построение замкнутых контуров и поворот цилиндра"):
    code_8 = """
    // Контур прямоугольника
    Line Loop(1) = {1, 2, 3, 4};

    // Контур круга
    Line Loop(2) = {5, 6, 7, 8};

    Rotate {{0, 0, 1}, {l, h, 0}, Pi / 4} {
            Curve{5, 6, 7, 8}; // Вращаем все дуги круга
    }

    // Плоская поверхность с вырезом
    Plane Surface(1) = {1, 2};
    """
    show_code(code_8, "python")
with st.expander("Определение физических ГУ"):
    code_9 = """
    // Физические линии для границ
    Physical Line("1") = {1};           // Нижняя граница
    Physical Line("2") = {3};           // Верхняя граница
    Physical Line("3") = {4};           // Левая граница
    Physical Line("4") = {2};           // Правая граница
    Physical Line("5") = {5, 6, 7, 8};  // Граница круга

    // Физическая поверхность
    Physical Surface("1") = {1};
    """
    show_code(code_9, "python")
with st.expander("Построение сетки"):
    code_10 = """
    // Настройка сетки
    Mesh.CharacteristicLengthMin = dd;
    Mesh.CharacteristicLengthMax = d;
    Mesh 2;
    """
    show_code(code_10, "python")

result = ''
for i in range(1, 11):
    result += globals()[f'code_{i}']


def save_example_file():
    example_file_path = './sym_ellips.geo'
    with open(example_file_path, 'w') as f:
            f.write(result)
    return example_file_path

# Кнопка для загрузки и запуска примера
if st.button("Построение расчетной области 🔧"):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)