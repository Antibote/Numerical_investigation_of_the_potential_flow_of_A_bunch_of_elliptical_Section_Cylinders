SetFactory("OpenCASCADE");

// Размеры области
L = 1.0;
H = 1.0;

// Эллипсы
r = 0.125;
R = 0.275;

// Сетка
N = 30;
d = H / N;
dd = 0.05 * d;

// Ячейки
nx = 3;
ny = 3;
dx = L / nx;
dy = H / ny;

// Границы области
Point(1) = {0, 0, 0, d};
Point(2) = {L, 0, 0, d};
Point(3) = {L, H, 0, d};
Point(4) = {0, H, 0, d};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

Line Loop(1) = {1, 2, 3, 4};

// Эллипсы
ellipses_loops[] = {};
line_groups[][] = {{}, {}, {}}; // по строкам

For row In {1:ny}
  For i In {1:nx}
    n = (row - 1) * nx + i;
    xc = (i - 0.5) * dx;
    yc = (row - 0.5) * dy;

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
    line_groups[row - 1][] += {c + 0, c + 1, c + 2, c + 3};
  EndFor
EndFor

// Поверхность с отверстиями
Plane Surface(1) = {1, ellipses_loops[]};

// --- Разделительные горизонтальные линии ---
y_mid1 = dy;       // между 1 и 2 рядом
y_mid2 = 2 * dy;   // между 2 и 3 рядом

Point(2001) = {0, y_mid1, 0, d};
Point(2002) = {L, y_mid1, 0, d};
Line(2001) = {2001, 2002};

Point(2003) = {0, y_mid2, 0, d};
Point(2004) = {L, y_mid2, 0, d};
Line(2002) = {2003, 2004};

// Границы области
Physical Line(101) = {1}; // bottom
Physical Line(102) = {2}; // right
Physical Line(103) = {3}; // top
Physical Line(104) = {4}; // left

// Эллипсы по строкам
Physical Line(201) = {line_groups[0][]}; // нижний ряд
Physical Line(202) = {line_groups[1][]}; // средний ряд
Physical Line(203) = {line_groups[2][]}; // верхний ряд

// Горизонтальные разделительные линии
Physical Line(301) = {2001}; // между первым и вторым рядом
Physical Line(302) = {2002}; // между вторым и третьим рядом

// Область
Physical Surface(401) = {1};

// Сетка
Mesh 2;
