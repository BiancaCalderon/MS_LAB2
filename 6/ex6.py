
# -------------------------
# MÉTODO DE BISECCIÓN
# -------------------------
def bisection(f, a, b, max_iter=100, tol=1e-7):
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos")

    approximations = []

    for _ in range(max_iter):
        c = (a + b) / 2
        approximations.append(c)

        if abs(f(c)) < tol or abs(b - a) / 2 < tol:
            return approximations, c

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    return approximations, c


# -------------------------
# MÉTODO DE LA SECANTE
# -------------------------
def secant(f, x0, x1, max_iter=100, tol=1e-7):
    approximations = [x0, x1]

    for _ in range(max_iter):
        fx0 = f(x0)
        fx1 = f(x1)

        if abs(fx1 - fx0) < 1e-12:
            break  # evitar división por cero

        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        approximations.append(x2)

        if abs(x2 - x1) < tol:
            return approximations, x2

        x0, x1 = x1, x2

    return approximations, x2


# -------------------------
# MÉTODO DE NEWTON-RAPHSON
# -------------------------
def newton(f, df, x0, max_iter=100, tol=1e-7):
    approximations = [x0]

    for _ in range(max_iter):
        dfx = df(x0)
        if abs(dfx) < 1e-12:
            break  # evitar división por cero

        x1 = x0 - f(x0) / dfx
        approximations.append(x1)

        if abs(x1 - x0) < tol:
            return approximations, x1

        x0 = x1

    return approximations, x1


# -------------------------
# Funcion de ejercicio 6
# -------------------------

def f(x):
    return 2*x**5 + 3*x**4 - 3*x**3 - 10*x**2 - 4*x + 4

def df(x):
    return 10*x**4 + 12*x**3 - 9*x**2 - 20*x - 4



print("=== EJERCICIO 6 ===")

roots = []

intervals = [(-3, -2), (-2, -1), (-1, 0), (0, 1), (1, 2), (2, 3)]
for a, b in intervals:
    try:
        aprox, root = bisection(f, a, b)
        root_rounded = round(root, 7)
        if root_rounded not in roots:
            roots.append(root_rounded)
            print(f"Bisección en [{a}, {b}]: raíz ≈ {root_rounded}, iteraciones = {len(aprox)}")
    except ValueError:
        pass

print("\n Newton-Raphson con diferentes puntos iniciales:")
tested_points = [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
for x0 in tested_points:
    try:
        aprox, root = newton(f, df, x0)
        root_rounded = round(root, 7)
        if root_rounded not in roots:
            roots.append(root_rounded)
            print(f"Newton desde x0 = {x0}: raíz ≈ {root_rounded}, iteraciones = {len(aprox)}")
    except:
        pass

print("\nRaíces reales aproximadas (únicas):")
print(sorted(roots))
