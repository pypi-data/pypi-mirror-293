def saludo():
    return "hola profe Germán"

def hola():
    return "Hola Danna"

def cumple_majito():
    return "Felizzzzz cumpleeee Majitoooo, que te vayaaa muy bienn hoy y te den muchosss regalosss."

def simplex(c, A, b):
    num_vars = len(c)
    num_constraints = len(b)

    # Crear la tabla inicial (matriz simplex)
    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    
    # Llenar la fila de costos
    tableau[0, :num_vars] = -c
    
    # Llenar la matriz A y los coeficientes de b
    tableau[1:, :num_vars] = A
    tableau[1:, num_vars:num_vars+num_constraints] = np.eye(num_constraints)
    tableau[1:, -1] = b

    # Imprimir la tabla inicial
    print("Tabla Inicial:")
    print(tableau)

    # Método Simplex
    while np.any(tableau[0, :-1] < 0):
        # Columna pivote (más negativa en la fila de costos)
        pivot_col = np.argmin(tableau[0, :-1])
        print(f"\nColumna pivote: {pivot_col}")
        
        # Fila pivote (mínima razón positiva entre b y columna pivote)
        ratios = tableau[1:, -1] / tableau[1:, pivot_col]
        pivot_row = np.argwhere(ratios == np.min(ratios[ratios > 0]))[0, 0] + 1
        print(f"Fila pivote: {pivot_row}")

        # Pivoteo
        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_element

        for i in range(tableau.shape[0]):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

        # Imprimir la tabla en cada iteración
        print("\nTabla después de la iteración:")
        print(tableau)

    # Resultado final
    print("\nSolución óptima encontrada:")
    solution = np.zeros(num_vars)
    for i in range(num_vars):
        col = tableau[1:, i]
        if np.sum(col == 1) == 1 and np.sum(col) == 1:
            solution[i] = tableau[np.where(col == 1)[0][0] + 1, -1]
    
    print(f"Variables de decisión: {solution}")
    print(f"Valor óptimo: {tableau[0, -1]}")


def ayudita():
    print(f"""
    from pulp import LpMaximize, LpProblem, LpVariable, lpSum

    # Crear el problema de maximización
    prob = LpProblem("Problema_de_produccion", LpMaximize)

    # Definir variables de decisión (enteras no binarias)
    x_A = LpVariable('x_A', lowBound=0, cat='Integer')
    x_B = LpVariable('x_B', lowBound=0, cat='Integer')
    x_C = LpVariable('x_C', lowBound=0, cat='Integer')

    # Función objetivo
    prob += 7 * x_A + 6 * x_B + 8* x_C, "Beneficio_Total"

    # Restricciones de las máquinas
    prob += 3 * x_A + 2 * x_B + 4* x_C <= 15, "Restriccion_Maquina_1"
    prob += 2 * x_A + 5* x_B + 3* x_C <= 20, "Restriccion_Maquina_2"
    prob += 4 * x_A + 3* x_B + 2* x_C <= 25, "Restriccion_Maquina_3"


    # Resolver el problema
    prob.solve()

    # Imprimir resultados
    print("Estado:", prob.status)
          
    print("prob.objective.value()", "x_A.value()")
    """)
    
    print("De minimización a maximimización las variables cambian las restricciones y las restricciones mantienen a las variables")

    print("np.linalg.inv(m)")

def ayudita2():
    print("Relaciones entre Primal y Dual:\n")

    print("1. Si el Primal es 'no-acotado', entonces:")
    print("   - El Dual es 'infactible'.\n")

    print("2. Si el Primal tiene solución óptima, entonces:")
    print("   - El Dual tiene solución óptima con los mismos valores.\n")

    print("3. Si el Primal es 'infactible', entonces:")
    print("   - El Dual puede ser 'no-acotado' o 'infactible'.")
    print("   - El Dual también puede ser 'posible'.\n")

    print("4. Si el Primal tiene solución óptima, el Dual también tiene solución óptima y los valores son los mismos.\n")

    print("5. Si el Primal es 'infactible', entonces el Dual puede ser 'posible'.\n")

    print("Dualidad debil Z(X) <= W(X)")
    print("Dualidad fuerte 17=17")
    print("Primal X>0 <--> Dual S1=0,   primal S1=0 <--> Dual y1>0")

def ayudita3():
    print(""" 
    for i in range(32):
    # Convertimos el número 'i' en binario y rellenamos con ceros a la izquierda para que tenga 5 dígitos
    bi = format(i, '05b')
    
    operacion = (20000*int(bi[0])) + (25000*int(bi[1])) + (15000*int(bi[2])) + (30000*int(bi[3])) + (10000*int(bi[4]))
    
    cumple = "Cumple" if operacion <= 50000 else "No"

    print(bi, cumple))
          """)