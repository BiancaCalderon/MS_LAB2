#Suponga ahora que la demanda diaria en el ´area 3 disminuye a 4 millones de galones. La producci´on excedente en las
#refiner´ıas 1 y 2 se env´ıa a otras ´areas de distribuci´on por medio de camiones. El costo de transporte por 100 galones
#es de $1.50 desde la refiner´ıa 1 y de $2.20 desde la refiner´ıa 2. La refiner´ıa 3 puede enviar su producci´on excedente a
#otros procesos qu´ımicos dentro de la planta.
#Formule y resuelva de nuevo el programa ´optimo de env´ıos
import pulp as pl

# Conjuntos
refinerias = ['R1', 'R2', 'R3']
areas = ['A1', 'A2', 'A3']

# Nuevas demandas
demanda_mod = {
    'A1': 4,
    'A2': 8,
    'A3': 4  # reducida de 7 a 4
}

# Capacidad de refinerías (igual)
oferta = {
    'R1': 6,
    'R2': 5,
    'R3': 8
}

# Distancias válidas
distancias = {
    ('R1', 'A1'): 120,
    ('R1', 'A2'): 180,
    # R1 - A3 no permitido
    ('R2', 'A1'): 300,
    ('R2', 'A2'): 100,
    ('R2', 'A3'): 80,
    ('R3', 'A1'): 200,
    ('R3', 'A2'): 250,
    ('R3', 'A3'): 120
}

# Costos camión por millón
costos_camion = {
    ('R1', 'A1'): 15,
    ('R1', 'A2'): 15,
    ('R2', 'A1'): 22,
    ('R2', 'A2'): 22
}

# Modelo
model = pl.LpProblem("Transporte_modificado", pl.LpMinimize)

# Variables oleoducto
x = pl.LpVariable.dicts("x", distancias, lowBound=0)

# Variables camión (sólo para R1 y R2 a A1, A2)
y = pl.LpVariable.dicts("y", costos_camion, lowBound=0)

# Función objetivo: costo total (oleoducto + camión)
model += (
    pl.lpSum(x[i,j]*distancias[i,j]*0.1 for (i,j) in distancias) +
    pl.lpSum(y[i,j]*costos_camion[i,j] for (i,j) in costos_camion)
)

# Restricciones de oferta
for i in refinerias:
    model += (
        pl.lpSum(x[i,j] for (ii,j) in distancias if ii == i) +
        pl.lpSum(y[i,j] for (ii,j) in costos_camion if ii == i)
        <= oferta[i]
    ), f"Oferta_{i}"

# Restricciones de demanda
for j in areas:
    model += (
        pl.lpSum(x[i,j] for (i,jj) in distancias if jj == j) +
        pl.lpSum(y[i,j] for (i,jj) in costos_camion if jj == j)
        == demanda_mod[j]
    ), f"Demanda_{j}"

# Resolver
model.solve()

# Resultados
print(f"Status: {pl.LpStatus[model.status]}")
print("Envíos por oleoducto:")
for var in x:
    if x[var].varValue > 0:
        print(f"{var}: {x[var].varValue:.2f} millones")

print("\nEnvíos por camión:")
for var in y:
    if y[var].varValue > 0:
        print(f"{var}: {y[var].varValue:.2f} millones")

print(f"\nCosto total: ${pl.value(model.objective):.2f}")
