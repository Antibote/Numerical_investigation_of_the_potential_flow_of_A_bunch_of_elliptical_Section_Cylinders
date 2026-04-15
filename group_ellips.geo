
        // Размеры области
        L = 3.0; // Ширина области
        H = 3.0; // Высота области

        // Размеры эллипсов
        r = 0.125;
        R = 0.175;

        // Сетка и шаг
        N = 30;
        d = H / N;
        dd = 0.05 * d;

        // Количество эллипсов
        nx = 3;
        ny = 3;

        // Размер ячейки
        dx = L / nx;
        dy = H / ny;
        
        // Углы прямоугольника
        Point(1) = {0, 0, 0, d};
        Point(2) = {L, 0, 0, d};
        Point(3) = {L, H, 0, d};
        Point(4) = {0, H, 0, d};

        // Границы
        Line(1) = {1, 2}; // нижняя
        Line(2) = {2, 3}; // правая
        Line(3) = {3, 4}; // верхняя
        Line(4) = {4, 1}; // левая

        Line Loop(1) = {1, 2, 3, 4};

        // Общие списки
        ellipses_loops[] = {};
        ellipses_all_curves[] = {};

        line_group_id = 10;

        For j In {1:ny}
            ellipse_lines_row[] = {};
            For i In {1:nx}
                n = (j - 1) * nx + i;

                xc = (i - 0.5) * dx;
                yc = (j - 0.5) * dy;

                p = 10 * n;
                c = 1000 + 4 * n;

                Point(p + 0) = {xc, yc, 0, dd};
                Point(p + 1) = {xc + R, yc, 0, dd};
                Point(p + 2) = {xc, yc + r, 0, dd};
                Point(p + 3) = {xc - R, yc, 0, dd};
                Point(p + 4) = {xc, yc - r, 0, dd};

                Ellipse(c + 0) = {p + 1, p + 0, p + 2};
                Ellipse(c + 1) = {p + 2, p + 0, p + 3};
                Ellipse(c + 2) = {p + 3, p + 0, p + 4};
                Ellipse(c + 3) = {p + 4, p + 0, p + 1};

                Rotate {{0, 0, 1}, {xc, yc, 0}, Pi/4} {
                    Curve{c + 0 : c + 3};
                }

                Line Loop(n + 1) = {c + 0, c + 1, c + 2, c + 3};
                ellipses_loops[] += {n + 1};
                ellipses_all_curves[] += {c + 0, c + 1, c + 2, c + 3};
                ellipse_lines_row[] += {c + 0, c + 1, c + 2, c + 3};
            EndFor

            // Физическая группа строк эллипсов с уникальным числовым идентификатором
            Physical Line(line_group_id) = {ellipse_lines_row[]};
            line_group_id += 1;
        EndFor
        
        // Поверхность с отверстиями
        Plane Surface(1) = {1, ellipses_loops[]};
        
        // Границы
        Physical Line(101) = {1}; // bottom
        Physical Line(102) = {2}; // right
        Physical Line(103) = {3}; // top
        Physical Line(104) = {4}; // left

        // Основная поверхность
        Physical Surface(201) = {1};
        
        // Построение сетки
        Mesh 2;
        