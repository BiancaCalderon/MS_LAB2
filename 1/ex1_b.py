# Usando JuMP o Pupl, determine el programa de env´ıos ´optimo en la red de distribución
import pulp as pl

# Conjuntos
refinerias = ['R1', 'R2', 'R3']
areas = ['A1', 'A2', 'A3']

# Capacidad de las refinerías (millones)
oferta = {
    'R1': 6,
    'R2': 5,
    'R3': 8
}

# Demanda de las áreas (millones)
demanda = {
    'A1': 4,
    'A2': 8,
    'A3': 7
}

# Distancias (en km)
distancias = {
    ('R1', 'A1'): 120,
    ('R1', 'A2'): 180,
    # R1-A3 no existe (infinito)
    ('R2', 'A1'): 300,
    ('R2', 'A2'): 100,
    ('R2', 'A3'): 80,
    ('R3', 'A1'): 200,
    ('R3', 'A2'): 250,
    ('R3', 'A3'): 120
}

# Crear modelo
model = pl.LpProblem("Transporte", pl.LpMinimize)

# Variables
x = pl.LpVariable.dicts("x", distancias, lowBound=0)

# Función objetivo: costo total (millones * km * $0.1 / 1000)
model += pl.lpSum(x[i,j]*distancias[i,j]*0.1 for (i,j) in distancias)

# Restricciones de oferta
for i in refinerias:
    model += pl.lpSum(x[i,j] for (ii,j) in distancias if ii == i) <= oferta[i], f"Oferta_{i}"

# Restricciones de demanda
for j in areas:
    model += pl.lpSum(x[i,j] for (i,jj) in distancias if jj == j) == demanda[j], f"Demanda_{j}"

# Resolver
model.solve()

# Resultado
print(f"Status: {pl.LpStatus[model.status]}")
print("Envíos óptimos:")
for var in x:
    if x[var].varValue > 0:
        print(f"{var}: {x[var].varValue:.2f} millones")
print(f"Costo total: ${pl.value(model.objective):.2f}")
