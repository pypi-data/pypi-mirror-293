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
