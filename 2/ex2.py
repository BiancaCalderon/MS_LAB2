#Problema de asignación
import pulp

# Definir los datos del problema
# Matriz de costos (Trabajadores x Trabajos)
costos = [
    [3, 8, 2, 10, 3, 3, 9],   # T1
    [2, 2, 7, 6, 5, 2, 7],    # T2
    [5, 6, 4, 5, 6, 6, 6],    # T3
    [4, 2, 7, 5, 9, 4, 7],    # T4
    [10, 3, 8, 4, 2, 3, 5],   # T5
    [3, 5, 4, 2, 3, 7, 8]     # T6
]

# Definir conjuntos
trabajadores = range(len(costos))           # [0, 1, 2, 3, 4, 5]
trabajos = range(len(costos[0]))           # [0, 1, 2, 3, 4, 5, 6]

print("=== PROBLEMA DE ASIGNACIÓN CON PuLP ===\n")
print("Matriz de costos:")
print("     ", end="")
for j in trabajos:
    print(f"  J{j+1:2}", end="")
print()

for i in trabajadores:
    print(f"T{i+1:2}:", end="")
    for j in trabajos:
        print(f"  ${costos[i][j]:2}", end="")
    print()
print()

# problema de optimización
problema = pulp.LpProblem("Problema_Asignacion", pulp.LpMinimize)

x = {}
for i in trabajadores:
    for j in trabajos:
        x[i, j] = pulp.LpVariable(f"x_{i+1}_{j+1}", cat='Binary')

# Función objetivo: minimizar el costo total
problema += pulp.lpSum([costos[i][j] * x[i, j] 
                       for i in trabajadores 
                       for j in trabajos]), "Costo_Total"

# Restricciones:
# 1. Cada trabajador debe ser asignado a exactamente un trabajo
for i in trabajadores:
    problema += pulp.lpSum([x[i, j] for j in trabajos]) == 1, f"Trabajador_{i+1}_asignado"

# 2. Cada trabajo puede ser asignado a máximo un trabajador
for j in trabajos:
    problema += pulp.lpSum([x[i, j] for i in trabajadores]) <= 1, f"Trabajo_{j+1}_maximo_uno"

# Resolver el problema
print("Resolviendo el problema...")
problema.solve(pulp.PULP_CBC_CMD(msg=0))  # msg=0 para suprimir mensajes del solver

# Mostrar resultados
print(f"\nEstado de la solución: {pulp.LpStatus[problema.status]}")

if problema.status == pulp.LpStatusOptimal:
    print("\n=== SOLUCIÓN ÓPTIMA ===")
    
    # Mostrar las asignaciones
    asignaciones = []
    costo_total = 0
    trabajos_asignados = []
    
    for i in trabajadores:
        for j in trabajos:
            if x[i, j].varValue == 1:
                costo = costos[i][j]
                asignaciones.append((i+1, j+1, costo))
                trabajos_asignados.append(j+1)
                costo_total += costo
                print(f"Trabajador T{i+1} → Trabajo J{j+1} (Costo: ${costo})")
    
    print(f"\nCosto total mínimo: ${costo_total}")
    
    # Mostrar trabajos no asignados
    trabajos_no_asignados = [j+1 for j in trabajos if (j+1) not in trabajos_asignados]
    if trabajos_no_asignados:
        print(f"Trabajos sin asignar: J{', J'.join(map(str, trabajos_no_asignados))}")
    
    print("\n=== MATRIZ DE ASIGNACIÓN ===")
    print("(1 = asignado, 0 = no asignado)")
    print("     ", end="")
    for j in trabajos:
        print(f"  J{j+1:2}", end="")
    print()
    
    for i in trabajadores:
        print(f"T{i+1:2}:", end="")
        for j in trabajos:
            valor = int(x[i, j].varValue) if x[i, j].varValue is not None else 0
            print(f"   {valor:2}", end="")
        print()
    
    print("\n=== VERIFICACIÓN ===")
    # Verificar restricciones
    print("Verificando restricciones:")
    
    # Cada trabajador asignado exactamente una vez
    for i in trabajadores:
        suma = sum(x[i, j].varValue or 0 for j in trabajos)
        print(f"Trabajador T{i+1}: {suma} asignación(es)" if suma == 1 else f"Trabajador T{i+1}: {suma} asignación(es) ✗")
    
    # Cada trabajo asignado máximo una vez
    for j in trabajos:
        suma = sum(x[i, j].varValue or 0 for i in trabajadores)
        status = "✓" if suma <= 1 else "X"
        if suma == 0:
            print(f"Trabajo J{j+1}: sin asignar")
        else:
            print(f"Trabajo J{j+1}: {suma} asignación(es) {status}")

else:
    print("No se encontró solución óptima")
    print(f"Estado: {pulp.LpStatus[problema.status]}")

print("\n=== INFORMACIÓN ADICIONAL ===")
print(f"Número de trabajadores: {len(trabajadores)}")
print(f"Número de trabajos disponibles: {len(trabajos)}")
print(f"Tipo de problema: {'Balanceado' if len(trabajadores) == len(trabajos) else 'Desbalanceado'}")
print(f"Variables de decisión creadas: {len(trabajadores) * len(trabajos)}")
print(f"Restricciones: {len(trabajadores) + len(trabajos)}")
