import math
import matplotlib.pyplot as plt

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
# Funcion de ejercicio 5
# -------------------------
def g(x):
    return x**2 + 1 / (x - 7)

def dg(x):
    return 2*x - 1 / (x - 7)**2


if __name__ == "__main__":
    print("=== EJERCICIO 5 ===")

    def g(x): return x**2 + 1 / (x - 7)
    def dg(x): return 2*x - 1 / (x - 7)**2

    
    print("\n--- MÉTODO DE BISECCIÓN ---")
    aprox_bis, root_bis = bisection(g, -2, 0)
    print(f"Raíz: {root_bis:.10f}, Iteraciones: {len(aprox_bis)}")

    print("\n--- MÉTODO DE LA SECANTE ---")
    aprox_sec, root_sec = secant(g, -2, 0)
    print(f"Raíz: {root_sec:.10f}, Iteraciones: {len(aprox_sec)}")

    print("\n--- MÉTODO DE NEWTON-RAPHSON ---")
    aprox_newton, root_newton = newton(g, dg, -1.5)
    print(f"Raíz: {root_newton:.10f}, Iteraciones: {len(aprox_newton)}")

    # Graficar convergencia
    plt.plot(aprox_bis, label="Bisección", marker='o')
    plt.plot(aprox_sec, label="Secante", marker='x')
    plt.plot(aprox_newton, label="Newton-Raphson", marker='s')
    plt.xlabel("Iteración")
    plt.ylabel("Aproximación")
    plt.title("Convergencia de métodos para g(x)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
