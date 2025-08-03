import numpy as np

def newton_multidimensional(F, J, x0, tol=1e-7, max_iter=100):
    """
    Método de Newton para funciones F: R^n → R^n.
    Parámetros:
      - F: función que toma un vector x (n,) y devuelve un vector F(x) (n,)
      - J: función que toma x y devuelve la matriz Jacobiana J(x) (n×n)
      - x0: punto inicial (array de longitud n)
      - tol: tolerancia para la norma de la corrección
      - max_iter: número máximo de iteraciones
    Devuelve:
      - xs: lista de aproximaciones (cada elemento es un array de longitud n)
      - x: aproximación final (array de longitud n)
    """
    x = x0.astype(float)
    xs = [x.copy()]
    for k in range(max_iter):
        Fx = F(x)
        Jx = J(x)
        # resolver J(x) · delta = -F(x)
        try:
            delta = np.linalg.solve(Jx, -Fx)
        except np.linalg.LinAlgError:
            raise RuntimeError(f"Jacobiano singular en iteración {k}")
        x = x + delta
        xs.append(x.copy())
        if np.linalg.norm(delta, ord=2) < tol:
            break
    return xs, x

# Definimos el sistema de ecuaciones dado:
#  1) 3x - cos(y z) - 1/2 = 0
#  2) x^2 - 81(y + 0.1)^2 + sin(z) + 1.06 = 0
#  3) e^{-x y} + 20 z + 10π - 3/3 = 0

def F_sys(x):
    X, Y, Z = x
    return np.array([
        3*X - np.cos(Y*Z) - 0.5,
        X**2 - 81*(Y + 0.1)**2 + np.sin(Z) + 1.06,
        np.exp(-X*Y) + 20*Z + 10*np.pi - 1  # obs: (10π - 3/3) = 10π - 1
    ])

def J_sys(x):
    X, Y, Z = x
    # derivadas parciales:
    # ∂/∂x [3x - cos(yz) - 0.5] = 3
    # ∂/∂y [3x - cos(yz) - 0.5] = -(-sin(yz)*z) =  sin(yz)*z
    # ∂/∂z [3x - cos(yz) - 0.5] = sin(yz)*y
    # ∂/∂x [x^2 - 81(y+0.1)^2 + sin(z) + 1.06] = 2x
    # ∂/∂y […] = -162*(y + 0.1)
    # ∂/∂z […] = cos(z)
    # ∂/∂x [e^{-xy} + 20z + 10π - 1] = -y * e^{-xy}
    # ∂/∂y […] = -x * e^{-xy}
    # ∂/∂z […] = 20
    return np.array([
        [3,                np.sin(Y*Z)*Z,     np.sin(Y*Z)*Y],
        [2*X,             -162*(Y + 0.1),      np.cos(Z)],
        [-Y*np.exp(-X*Y), -X*np.exp(-X*Y),     20      ]
    ])

# Elegimos un punto inicial razonable, por ejemplo:
x0 = np.array([1.0,  0.0,  0.0])

# Ejecutamos Newton multidimensional:
lista_iters, raiz = newton_multidimensional(F_sys, J_sys, x0)

print("Aproximaciones sucesivas:")
for i, xi in enumerate(lista_iters):
    print(f"  x_{i} = {xi}")
print("\nRaíz aproximada (7 decimales):", np.round(raiz, 7))

if __name__ == "__main__":
  # Punto inicial
  x0 = np.array([1.0, 0.0, 0.0])

  # Ejecutar Newton multidimensional
  lista_iters, raiz = newton_multidimensional(F_sys, J_sys, x0)

  # Mostrar resultados
  print("Aproximaciones sucesivas:")
  for i, xi in enumerate(lista_iters):
    print(f"  x_{i} = {xi}")
  print("\nRaíz aproximada (7 decimales):", np.round(raiz, 7))
