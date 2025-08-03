#Una empresa necesita asignar cuatro puestos de trabajo a cuatro trabajadores. El costo de desempe˜nar un puesto es una
#funci´on de las habilidades de los trabajadores. En la tabla siguiente se resume el costo de las asignaciones. El trabajador 1
#no puede tener el puesto 3, y el trabajador 3 no puede desempe˜nar el puesto 4. Determine la asignaci´on ´optima mediante
#programaci´on lineal.

import pulp

# Definir los datos del problema
# Matriz de costos (Trabajadores x Puestos de Trabajo)
# Interpretando la tabla: 4 trabajadores, 4 puestos
costos = [
    [50, 50, float('inf'), 20],  # Trabajador 1 (no puede hacer puesto 3)
    [70, 40, 20, 30],            # Trabajador 2  
    [90, 30, 50, float('inf')],  # Trabajador 3 (no puede hacer puesto 4)
    [70, 20, 60, 70]             # Trabajador 4
]

# Reemplazamos infinito con un valor muy alto
VALOR_PROHIBIDO = 999999
for i in range(len(costos)):
    for j in range(len(costos[i])):
        if costos[i][j] == float('inf'):
            costos[i][j] = VALOR_PROHIBIDO

# Definir conjuntos
trabajadores = range(len(costos))        # [0, 1, 2, 3]
puestos = range(len(costos[0]))         # [0, 1, 2, 3]

print("=== PROBLEMA DE ASIGNACIÓN DE EMPRESA ===\n")
print("Una empresa necesita asignar 4 puestos de trabajo a 4 trabajadores.")
print("Restricción: Trabajador 1 no puede hacer puesto 3")
print("Restricción: Trabajador 3 no puede hacer puesto 4")
print()

print("Matriz de costos:")
print("           ", end="")
for j in puestos:
    print(f"Puesto {j+1:2}", end="")
print()

for i in trabajadores:
    print(f"Trabajador {i+1:2}:", end="")
    for j in puestos:
        if costos[i][j] == VALOR_PROHIBIDO:
            print("    ---", end="")
        else:
            print(f"   ${costos[i][j]:3}", end="")
    print()
print()

# Crear el problema de optimización
problema = pulp.LpProblem("Asignacion_Empresa", pulp.LpMinimize)

# Variables de decisión: x[i][j] = 1 si trabajador i se asigna a puesto j
x = {}
for i in trabajadores:
    for j in puestos:
        x[i, j] = pulp.LpVariable(f"x_T{i+1}_P{j+1}", cat='Binary')

# Función objetivo: minimizar el costo total
problema += pulp.lpSum([costos[i][j] * x[i, j] 
                       for i in trabajadores 
                       for j in puestos]), "Costo_Total"

# Restricciones:
# 1. Cada trabajador debe ser asignado a exactamente un puesto
for i in trabajadores:
    problema += pulp.lpSum([x[i, j] for j in puestos]) == 1, f"Trabajador_{i+1}_un_puesto"

# 2. Cada puesto debe ser asignado a exactamente un trabajador  
for j in puestos:
    problema += pulp.lpSum([x[i, j] for i in trabajadores]) == 1, f"Puesto_{j+1}_un_trabajador"

# 3. Restricciones específicas (ya manejadas con costos muy altos)
# Trabajador 1 no puede hacer puesto 3
# Trabajador 3 no puede hacer puesto 4

print("Resolviendo el problema...")
problema.solve(pulp.PULP_CBC_CMD(msg=0))

# Mostrar resultados
print(f"\nEstado de la solución: {pulp.LpStatus[problema.status]}")

if problema.status == pulp.LpStatusOptimal:
    print("\n=== SOLUCIÓN ÓPTIMA ===")
    
    # Mostrar las asignaciones
    asignaciones = []
    costo_total = 0
    
    for i in trabajadores:
        for j in puestos:
            if x[i, j].varValue == 1:
                costo_real = 50 if i == 0 and j == 0 else \
                           50 if i == 0 and j == 1 else \
                           20 if i == 0 and j == 3 else \
                           70 if i == 1 and j == 0 else \
                           40 if i == 1 and j == 1 else \
                           20 if i == 1 and j == 2 else \
                           30 if i == 1 and j == 3 else \
                           90 if i == 2 and j == 0 else \
                           30 if i == 2 and j == 1 else \
                           50 if i == 2 and j == 2 else \
                           70 if i == 3 and j == 0 else \
                           20 if i == 3 and j == 1 else \
                           60 if i == 3 and j == 2 else \
                           70 if i == 3 and j == 3 else 0
                
                asignaciones.append((i+1, j+1, costo_real))
                costo_total += costo_real
                print(f"Trabajador {i+1} → Puesto {j+1} (Costo: ${costo_real})")
    
    print(f"\nCosto total mínimo: ${costo_total}")
    
    print("\n=== MATRIZ DE ASIGNACIÓN ===")
    print("(1 = asignado, 0 = no asignado)")
    print("           ", end="")
    for j in puestos:
        print(f"  P{j+1:2}", end="")
    print()
    
    for i in trabajadores:
        print(f"T{i+1:2}:", end="")
        for j in puestos:
            valor = int(x[i, j].varValue) if x[i, j].varValue is not None else 0
            print(f"   {valor:2}", end="")
        print()
    
    print("\n=== VERIFICACIÓN DE RESTRICCIONES ===")
    
    # Verificar que cada trabajador tiene un puesto
    print("Cada trabajador asignado a un puesto:")
    for i in trabajadores:
        suma = sum(x[i, j].varValue or 0 for j in puestos)
        print(f"  Trabajador {i+1}: {suma} puesto(s)" if suma == 1 else f"  Trabajador {i+1}: {suma} puesto(s) ✗")
    
    # Verificar que cada puesto tiene un trabajador
    print("\nCada puesto asignado a un trabajador:")
    for j in puestos:
        suma = sum(x[i, j].varValue or 0 for i in trabajadores)
        print(f"  Puesto {j+1}: {suma} trabajador(es)" if suma == 1 else f"  Puesto {j+1}: {suma} trabajador(es) ✗")
    
    # Verificar restricciones específicas
    print("\nRestricciones específicas:")
    t1_p3 = x[0, 2].varValue or 0
    t3_p4 = x[2, 3].varValue or 0
    
    print(f"  Trabajador 1 NO asignado a Puesto 3: {'✓' if t1_p3 == 0 else 'X'}")
    print(f"  Trabajador 3 NO asignado a Puesto 4: {'✓' if t3_p4 == 0 else 'X'}")

else:
    print("No se encontró solución óptima")
    print(f"Estado: {pulp.LpStatus[problema.status]}")

print("\n=== ANÁLISIS DE LA SOLUCIÓN ===")
if problema.status == pulp.LpStatusOptimal:
    print("Beneficios de la asignación óptima:")
    print("• Todos los puestos están cubiertos")
    print("• Todos los trabajadores tienen asignación")
    print("• Se respetan las restricciones de incompatibilidad")
    print("• Se minimiza el costo total de la empresa")
    print(f"• Costo promedio por asignación: ${costo_total/4:.2f}")

print(f"\nInformación del problema:")
print(f"• Número de trabajadores: {len(trabajadores)}")
print(f"• Número de puestos: {len(puestos)}")
print(f"• Tipo: Problema balanceado (misma cantidad de trabajadores y puestos)")
print(f"• Variables de decisión: {len(trabajadores) * len(puestos)}")
print(f"• Restricciones: {len(trabajadores) + len(puestos)} (más las de incompatibilidad)")