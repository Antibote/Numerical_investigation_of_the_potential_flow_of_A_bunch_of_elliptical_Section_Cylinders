import streamlit as st

menu = st.sidebar.radio('***',
    ("Комплексный потенциал течения", 
    "Критические точки",       
    "Аналитическое решение",
    "Решение методом конечных элементов (FEniCS)",
    "Циркулляция по контуру цилиндра",
    "Программная реализация",
    )
)

if menu == "Комплексный потенциал течения":
    r"""
    ##### Комплексный потенциал течения
    """

    st.image("teor_1.png", caption="",use_container_width=True)

    st.image("teor.png", caption="",use_container_width=True)
    
    r"""
    Пусть эллипс обтекается идеальной жидкостью со скоростью $u_{\infty} e^{i \alpha}$

    Комплексный потенциал в параметрическом виде

    $\begin{aligned}
    w = \frac{u_{\infty}}{2} \left( e^{-i \alpha} t + \frac{e^{i \alpha} R_t^2}{t} \right) + \frac{\Gamma}{2 \pi i} \ln{t}, \quad R_t = R + r
    \end{aligned}$
    
    **Преобразование Жуковского**

    $\begin{aligned}
    z = \frac{1}{2} \left(t + \frac{c^2}{t}\right), \quad c = \sqrt{R^2 - r^2}, \quad R \ge r
    \end{aligned}$

    в симметричном виде

    $\begin{aligned}
    \frac{z - c}{z + c} = \left( \frac{t - c}{t + c} \right)^2
    \end{aligned}$

     * $R_t$ -- ридиус параметрического круга

     * $R$ -- большая полуось эллипса

     * $r$ -- малая полуось эллипса

     * $\alpha$ -- угол атаки

     * $\begin{aligned}
       u_{\infty} = u_{x_1} + i u_{x_2}
       \end{aligned}$

     * $\begin{aligned}
       z = x_1 + i x_2
       \end{aligned}$

    Исключим параметр $t$

    $\begin{aligned}
    t^2 - 2zt + c^2 = 0, \quad t = z + \sqrt{z^2 - c^2}
    \end{aligned}$

    Если взять корень со знаком минус, то внешность эллипса перейдет во внутренность параметрического круга.

    $\begin{aligned}
    w = \frac{u_{\infty}}{2} \left( e^{-i \alpha} \left(z + \sqrt{z^2 - c^2}\right)  + \frac{e^{i \alpha} R_t^2}{\left(z + \sqrt{z^2 - c^2}\right)} \right) + \frac{\Gamma}{2 \pi i} \ln{\left(z + \sqrt{z^2 - c^2}\right)}
    \end{aligned}$ 
    """
    with st.expander("Функция комплексного потенциала и комплексно-сопряженной скорости"):
        code = """
            def t(z):
                return z + np.sqrt(z - c) * np.sqrt(z + c)
    
            def w(z, Gamma):
                return (vinff / 2 * (np.exp(-1j * alpha1) * t(z) + (np.exp(1j * alpha1) * r**2) / t(z)) +
                        (Gamma * np.log(t(z))) / (2 * np.pi * 1j))
    
            def w_prime(z, Gamma):
                h = 1e-8
                return (w(z + h, Gamma) - w(z - h, Gamma)) / (2 * h)
        """

        st.code(code, language="python")

    r"""
    ##### Комплексно-сопряженная скорость

    $\begin{aligned}
    \frac{d w}{d z} = \frac{u_{\infty}}{2} \left( e^{-i \alpha} \left(1 + \frac{z}{\sqrt{z^2 - c^2}} \right)  + \frac{e^{i \alpha} R_t^2 \left(1 + \frac{z}{\sqrt{z^2 - c^2}}\right)}{\left(z + \sqrt{z^2 - c^2}\right)^2} \right) + \frac{\Gamma}{2 \pi i} \frac{\left(1 + \frac{z}{\sqrt{z^2 - c^2}} \right)}{\left(z + \sqrt{z^2 - c^2}\right)}
    \end{aligned}$

    $\begin{aligned}
    \frac{d w}{d z} = u_{x_1} - i u_{x_2} 
    \end{aligned}$

    $\begin{aligned}    
    \text{Re } \frac{d w}{ d z} = u_{x_1}
    \end{aligned}$

    $\begin{aligned}    
    \text{Im } \frac{d w}{ d z} = - u_{x_2}
    \end{aligned}$


    ##### Бесциркулляционное течение
    
    $\Gamma = 0$

    $\begin{aligned}
    w = \frac{u_{\infty}}{2} \left( e^{-i \alpha} \left(z + \sqrt{z^2 - c^2}\right)  + \frac{e^{i \alpha} R_t^2}{\left(z + \sqrt{z^2 - c^2}\right)} \right)
    \end{aligned}$

    $\begin{aligned}
    \frac{d w}{d z} = \frac{u_{\infty}}{2} \left( e^{-i \alpha} \left(1 + \frac{z}{\sqrt{z^2 - c^2}} \right)  + \frac{e^{i \alpha} R_t^2 \left(1 + \frac{z}{\sqrt{z^2 - c^2}}\right)}{\left(z + \sqrt{z^2 - c^2}\right)^2} \right)
    \end{aligned}$
    
    """

    with st.expander("Вычисление поля скоростей"):
        code = """
        
        Ux = np.ma.masked_invalid(Ux)
        Uy = np.ma.masked_invalid(Uy)

        speed = np.sqrt(np.abs(Ux)**2 + np.abs(Uy)**2)
        """

        st.code(code, language="python")


elif menu == "Критические точки":
    r"""
    ##### Критические точки

    Определим положение критических точек, решив уравнение
    
    $\begin{aligned}
    \frac{d w}{d z} = \frac{u_{\infty}}{2} \left( e^{-i \alpha} \left(1 + \frac{z}{\sqrt{z^2 - c^2}} \right)  + \frac{e^{i \alpha} R_t^2 \left(1 + \frac{z}{\sqrt{z^2 - c^2}}\right)}{\left(z + \sqrt{z^2 - c^2}\right)^2} \right) + \frac{\Gamma}{2 \pi i} \frac{\left(1 + \frac{z}{\sqrt{z^2 - c^2}} \right)}{\left(z + \sqrt{z^2 - c^2}\right)} = 0
    \end{aligned}$

    При $\Gamma = 0$

    $\begin{aligned}
    \frac{d w}{d z} = \frac{u_{\infty}}{2} \left( e^{-i \alpha} \left(1 + \frac{z}{\sqrt{z^2 - c^2}} \right)  + \frac{e^{i \alpha} R_t^2 \left(1 + \frac{z}{\sqrt{z^2 - c^2}}\right)}{\left(z + \sqrt{z^2 - c^2}\right)^2} \right) = 0
    \end{aligned}$

    """

    with st.expander("Поиск критических точек"):
        code = """
        def find_stagnation_point(initial_guess):
            def func(z_real_imag):
                z_complex = z_real_imag[0] + 1j * z_real_imag[1]
                w_p = w_prime(z_complex, Gamma)
                return [np.real(w_p), np.imag(w_p)]
            
            sol = root(func, [np.real(initial_guess), np.imag(initial_guess)], method='hybr')
            
            z_stag = sol.x[0] + 1j * sol.x[1]
            if (np.real(z_stag) ** 2 / a ** 2 + np.imag(z_stag) ** 2 / b1 ** 2) < 1:
                return None 
            return z_stag
            """

        st.code(code, language="python")

    
elif menu == "Аналитическое решение":
    r"""
    ##### Аналитическое решение
    """

    subtopic = st.selectbox(
        "Большая полуось эллипса",  
        ["R = 0.175", "R = 0.225", "R = 0.275"]  
    )

    if subtopic == "R = 0.175":

        st.image("Ellips_1.1.png", caption="",use_container_width=True)

        r"""
        ------------------------------------------------
        * Полуоси эллипса: $R = 0.175, \quad r = 0.125$
        * Скорость на входе: $u_{\infty} = 1$
        * Угол поворота цилиндра: $\alpha = \frac{\pi}{4}$

        ------------------------------------------------
        ##### Критические точки

         - $x_1 = 0.35, \quad x_2 = 0.475$
        
         - $x_1 = 0.65, \quad x_2 = 0.525$
        ------------------------------------------------
        ##### Циркулляция по контуру эллипса

         - $\Gamma = 0$
        """

    elif subtopic == "R = 0.225":

        st.image("Ellips_1.2.png", caption="",use_container_width=True)

        r"""
        -----------------------------------------------

        * Полуоси эллипса: $R = 0.225, \quad r = 0.125$
        * Скорость на входе: $u_{\infty} = 1$
        * Угол поворота цилиндра: $\alpha = \frac{\pi}{4}$

        ------------------------------------------------
        ##### Критические точки

         - $x_1 = 0.325, \quad x_2 = 0.45$
        
         - $x_1 = 0.675, \quad x_2 = 0.55$

        ------------------------------------------------
        ##### Циркулляция по контуру эллипса
        
         - $\Gamma = 0$
        """

    elif subtopic == "R = 0.275":

        st.image("Ellips_1.3.png", caption="",use_container_width=True)

        r"""
        ------------------------------------------------

        * Полуоси эллипса: $R = 0.275, \quad r = 0.125$
        * Скорость на входе: $u_{\infty} = 1$
        * Угол поворота цилиндра: $\alpha = \frac{\pi}{4}$

        ------------------------------------------------
        ##### Критические точки

         - $x_1 = 0.3, \quad x_2 = 0.425$
        
         - $x_1 = 0.7, \quad x_2 = 0.575$
        ------------------------------------------------
        ##### Циркулляция по контуру эллипса
         - $\Gamma = 0$
        """


    with st.expander("Вычисление циркулляции по контуру"):
        code = """
        
        dz = (x_ellipse[1:] - x_ellipse[:-1]) + 1j * (y_ellipse[1:] - y_ellipse[:-1])
        velocity = w_prime(x_ellipse[:-1] + 1j * y_ellipse[:-1], Gamma)
        circulation = np.sum(velocity * dz)
        """

        st.code(code, language="python")

elif menu == "Решение методом конечных элементов (FEniCS)":

    r"""

    ##### Решение методом конечных элементов (FEniCS)

    """

    subtopic = st.selectbox(
        "Большая полуось ",  
        ["R = 0.175", "R = 0.225", "R = 0.275"]  
    )

    if subtopic == "R = 0.175":

        st.image("ellips_0175.png", caption="",use_container_width=True)

        r"""
        ------------------------------------------------
        * Число ячеек сетки: 27298

        * Число узлов сетки: 14594

        ------------------------------------------------
        """
        st.image("ellips_solve_0175.png", caption="",use_container_width=True)
        r"""
        ------------------------------------------------
        * Циркулляция по контуру элипса: $9.88850*10^{-6}$
        """

    elif subtopic == "R = 0.225":

        st.image("ellips_0225.png", caption="",use_container_width=True)

        r"""
        ------------------------------------------------

        * Число ячеек сетки: 31802

        * Число узлов сетки: 16635

        ------------------------------------------------
        """
        st.image("ellips_solve_0225.png", caption="",use_container_width=True)

        r"""
        * Циркулляция по контуру эллипса: $1.07842*10^{-5}$
        """

    elif subtopic == "R = 0.275":

        st.image("ellips_0275.png", caption="",use_container_width=True)

        r"""
        -----------------------------------------------

        * Число ячеек сетки: 36174

        * Число узлов сетки: 18929

        ------------------------------------------------
        """
        st.image("ellips_solve_0275.png", caption="",use_container_width=True)

        r"""
        * Циркулляция по контуру эллипса: $2.25365*10^{-5}$
        """

elif menu == "Циркулляция по контуру цилиндра":

    r"""
    ##### Циркуляция и число степеней свободы в зависимости от R и порядка аппроксимации \(p\)

    | $R$     | Размер сетки | Циркуляция $p=1$       | Ст. свободы $p=1$ | Циркуляция $p=2$       | Ст. свободы $p=2$ | Циркуляция $p=3$       | Ст. свободы $p=3$ |
    |---------|--------------|------------------------|--------------------|------------------------|--------------------|------------------------|--------------------|
    | 0.175   | 14594        | $9.888 \cdot 10^{-6}$  | 14594              | $-2.986 \cdot 10^{-6}$ | 57116              | $-2.234 \cdot 10^{-6}$ | 127566             |
    | 0.225   | 16635        | $1.078 \cdot 10^{-5}$  | 16635              | $-1.313 \cdot 10^{-6}$ | 65072              | $-8.002 \cdot 10^{-7}$ | 145311             |
    | 0.275   | 18929        | $2.253 \cdot 10^{-5}$  | 18929              | $2.096 \cdot 10^{-6}$  | 74032              | $1.393 \cdot 10^{-6}$  | 165309             |
    """
        

elif menu == "Программная реализация":

    r"""
    ##### Программная реализация
    """

    with st.expander("Определение функционального пространства"):
        code = """
            pbc = PeriodicBoundary(L, H)
            V = FunctionSpace(mesh, 'CG', 1, constrained_domain=pbc)
        """

        st.code(code, language="python")

    with st.expander("Граничные условия"):
        code = """
        class PeriodicBoundary(SubDomain):
                def __init__(self, L, H):
                    super().__init__()
                    self.L = L  # Длина области по X
                    self.H = H  # Высота области по Y

                def inside(self, x, on_boundary):
                    # Проверяем, находится ли точка на левой ИЛИ нижней границе
                    return (near(x[0], 0.0) or (near(x[1], 0.0))) and on_boundary

                def map(self, x, y):
                    if near(x[0], self.L):  # Если точка на правой границе
                        y[0] = x[0] - self.L
                        y[1] = x[1]
                    elif near(x[1], self.H):  # Если точка на верхней границе
                        y[0] = x[0]
                        y[1] = x[1] - self.H
                    else:  # Иначе (левая/нижняя граница)
                        y[0] = x[0]
                        y[1] = x[1]

            class Psi0Expression(UserExpression):
                def eval(self, value, x):
                    value[0] = (x[1]/H)*psi0 - psi0/2  # Центрируем вокруг нуля
                
                def value_shape(self):
                    return ()
        """

        st.code(code, language="python")

    with st.expander("Вариационная задача"):
        code = """
            u = TrialFunction(V)
            v = TestFunction(V)
            f = Constant(0.0)
            a = dot(grad(u), grad(v)) * dx
            L = f * v * dx
        """

        st.code(code, language="python")

    with st.expander("Решение задачи"):
        code = """
            u = Function(V)
            solve(a == L, u)
        """

        st.code(code, language="python")

    with st.expander("Вычисление скорости"):
        code = """
            V_vector = VectorFunctionSpace(mesh, "CG", 3)
            velocity = project(grad(u), V_vector)
            velocity_magnitude = project(sqrt(dot(velocity, velocity)), V)
        """

        st.code(code, language="python")

    with st.expander("Вычисление циркуляции"):
        code = """
            n = FacetNormal(mesh)
            u_n = dot(grad(u), n)
            Gamma = assemble(u_n * ds(subdomain_data=boundaries, subdomain_id=5))
        """

        st.code(code, language="python")

    with st.expander("Поиск критических точек"):
        code = """
            threshold = 1e-15
            critical_points = (velocity_values < threshold)
            critical_x = x[critical_points]
            critical_y = y[critical_points]

        """

        st.code(code, language="python")

    with st.expander("Построение эллипса"):
        code = """
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

        """

        st.code(code, language="python")


    

    





    
