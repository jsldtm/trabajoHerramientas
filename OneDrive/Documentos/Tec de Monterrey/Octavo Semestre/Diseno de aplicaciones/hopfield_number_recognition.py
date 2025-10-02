## Por - Joaquin Saldarriaga; 30/09/25 - 01/10/25
## Neural Net. de Hopfield con reconocimiento de números en matrices
## sin librerías externas como Numpy, Scipy, o afines

## Elabora la Neural Net. de Hopfield realizada la semana anterior

## Importación de módulo 'os' para manejo de rutas de archivos
import os

## Definición de hiperparámetros de la Nerual Net.
MATRIX_ROWS = 8  ## Filas de la matriz (e.g., 8)
MATRIX_COLS = 5  ## Columnas de la matriz (e.g., 5)
N_NEURONS = MATRIX_ROWS * MATRIX_COLS

## Especificación de rutas de archivos 'ejemplares' & 'prueba'
TRAINING_FOLDER = "datasets" 
TEST_FILE_PATH = os.path.join(TRAINING_FOLDER, "x.txt")

## ******* Funciones de la Neural Net. original *******

## Definición de función para convertir a 'representación bipolar' [+1/-1]
def to_bipolar(v):
    
    ## Inicializar la lista resultante
    output_list = []  
    
    ## Itera elementos de entrada
    for i in range(len(v)):
        
        ## Si es 0, 'mapea' a *-1*
        if v[i] == 0:
            output_list.append(-1)
            
        ## Si es 1, 'mapea' a *+1*
        elif v[i] == 1: 
            output_list.append(1)
            
        ## Si ya es -1, lo conserva
        elif v[i] == -1: 
            output_list.append(-1)
            
        ## Si es otro valor positivo, resulta '+1'
        elif v[i] > 0:
            output_list.append(1)
        
        ## Si es otro valor *negativo*, resulta '-1'
        else:
            output_list.append(-1)
    
    ## Retorna vector bipolar
    return output_list

## Función para crear matriz 'n x n' de *ceros*
def zero_matrix(n):
    
    ## Inicializar matriz
    Zero_matrix = []
    
    ## Iterar para cada fila
    for i in range(n):
        
        ## Inicializar la fila en cuestión
        row = []
        
        ## Iterar para cada columna
        for j in range(n):
            ## Añadir un 'cero'
            row.append(0) 
            
        ## Añadir la 'fila' a la matriz
        Zero_matrix.append(row)
        
    ## Eventualmente, retornar la matriz creada
    return Zero_matrix

## Función para obtener el producto 'exterior' de dos vectores (i.e.; 'u * v^T')
def outer(u, v): 
    
    ## Inicializar la matriz resultante
    matrix_resultante = []
    
    ## Iterar por filas
    for i in range(len(u)):  # Filas
        row = []  # Fila temporal
        for j in range(len(v)):  # Columnas
            row.append(u[i] * v[j])  # Producto componente
        matrix_resultante.append(row)  # Añade fila
    return matrix_resultante  # Retorna matriz

## Función que suma la matrices 'B' y 'A' (operación 'in-place')
def add_inplace(A, B):  
    
    ## Se itera por cada fila de la matriz 'A'
    for i in range(len(A)):  
        
        ## Se itera por cada columna asumiendo *forma rectangular*
        for j in range(len(A[0])):
            
            ## Se realiza la suma elemento a elemento y se asigna en 'A'
            A[i][j] = A[i][j] + B[i][j]

# Función que construye la matriz de pesos a partir de una lista de patrones
def build_weights(patterns):
    
    ## Determinar el número de neuronas por la longitud del *primer patrón*
    neurons = len(patterns[0]) 
    
    ## Inicializar la matriz de 'weights' como una 'n x n' de ceros
    weight_matrix = zero_matrix(neurons)
    
    ## Se itera por cada patrón en la 'lista de patrones'
    for p in patterns:
        
        ## Calcula el producto exterior p * p^T para el patrón actual
        exterior_prod = outer(p, p)
        
        ## Acumular el 'prod. exterior' en 'weight_matrix'
        add_inplace(weight_matrix, exterior_prod)
    
    ## Iterar sobre la *diagonal* de 'weight_matrix' para no acumular el 'peso' propio
    for i in range(neurons): 
        ## Se fija cada 'elemento diagonal' a cero
        weight_matrix[i][i] = 0 
    
    ## Se retorna la 'weight_matrix' resultante
    return weight_matrix

## Función que multiplica una matriz por un vector (e.g.; 'W * v')
def matrix_vector_product(W, v): 
    ## Inicializar la lista que contendrá el 'vector resultante'
    output_vector = []
    
    ## Iterar por cada fila de la matriz 'W'
    for i in range(len(W)):
        
        ## Inicializar el *acumulador* de la suma para la fila 'i'
        s = 0 
        
        ## Iterar por 'cada' componente del vector 'v'
        for j in range(len(v)):
            
            ## Acumular el producto 'W[i][j] * v[j]' en el *acumulador*
            s = s + W[i][j] * v[j] 
        
        ## Añadir la suma resultante como componente 'i' del vector resultante
        output_vector.append(s)
        
    ## Retornar el vector resultante de la multiplicación
    return output_vector 

## Definir la 'función de activación' (escalón bipolar)
def activation_function(x, previous):
    
    ## Evaluar si la 'entrada neta' es estrictamente *positiva*
    if x > 0:  
        
        ## En tal caso, retornar +1
        return 1 
    
    ## Evaluar si la 'entrada neta' es estrictamente *negativa*
    if x < 0:
        ## En tal caso, retornar '-1'
        return -1 
    
    ## Retornar y mantener 'valor previo' cuando la 'entrada neta' es *cero*
    return previous

## Define el procedimiento de 'recall síncrono' hasta *convergencia*
def recall_sync(W, init, max_steps):
    
    ## Crear una 'copia local' del estado inicial
    state = [] 
    
    ## Iterar para copiar 'cada' componente del *vector inicial*
    for i in range(len(init)):
        
        ## Añadir el componente 'i' a la copia local del *estado*
        state.append(init[i])  
    
    ## Se inicializar el 'contador de iteraciones'
    steps_iteration = 0 
    
    ## Itera hasta alcanzar el número max. de pasos permitido
    while steps_iteration < max_steps:  
        
        ## Calcular el 'vector de entradas' netas 'W  * state'
        net = matrix_vector_product(W, state)
        
        ## Definir la lista de los nuevo estados actualizados
        new_state = [] 
        
        ## Itera por 'cada' neurona para aplicar la *f(x) de activación*
        for i in range(len(state)):
            
            ## Aplica la *f(x) de activación* con el 'estado anteior'
            new_state.append(activation_function(net[i], state[i]))
        
        ## Comprobar si el estado ha dejado de cambiar (i.e.; 'convergencia')
        if new_state == state:
            
            ## Retornar el estado convergido
            return new_state

        ## Actualizar el estado para la 'siguiente iteración'
        state = new_state
        
        ## Incrementar el 'contador' de iteraciones
        steps_iteration = steps_iteration + 1
    
    ## Retorna el 'estado final' en caso de que no se alcanzó convergencia en el número máximo de pasos
    return state

## FUnción que calcula el num. de posiciones distintas entre dos vectores
def diferencias_por_posicion(a, b):
    
    ## Inicializar el 'contador de diferencias'
    number_of_difs = 0
    
    ## Iterar por 'cada posición' del vector
    for i in range(len(a)): 
        
        ## Comprobar si los elementos difieren en la posición 'i'
        if a[i] != b[i]:  
            
            ## En tal caso, incrementar el 'contador de diferencias'
            number_of_difs = number_of_difs + 1  
    
    ## Eventualmente, retornar el 'número de diferencias' halladas
    return number_of_difs


## Función que asigna el 'estado recuperado' al *patrón almacenado* más cercano
def classify(recovered, stored):
    
    ## Inicializar el 'índice' del *mejor candidato* con cero
    best_pattern_index = 0
    
    ## Calcular la 'distancia inicial' con el *primer* patrón almacenado
    best_dist = diferencias_por_posicion(recovered, stored[0])
    
    ## Inicializa el iterador en '1' para evaluar los *patrones restantes*
    i = 1
    
    ## Iterar sobre los 'patrones almacenados' restantes
    while i < len(stored):
        
        ## Calcular las *diferencias_por_posicion* al patrón 'i'
        difs = diferencias_por_posicion(recovered, stored[i])
        
    ## Comprobar si la 'distancia actual' es menor que la *mejor observada*
        if difs < best_dist: 
            
            ## Actualizar la 'mejor distancia' observada
            best_dist = difs
            
            ## Actualiza el 'índice' del *patrón más cercano*
            best_pattern_index = i 
        
        ## Incrementa el iterador para examinar el 'siguiente' patrón
        i = i + 1
    
    ## Retornar el 'índice' del *patrón almacenado* más cercano
    return best_pattern_index

## Función que formatea un 'vector bipolar' para *impresión legible*
def format_vec(v):
    
    ## Inicializar la 'cadena reultante' con el corchete de apertura
    resulting_string = "["
    
    ## Inicializar el índice de recorrido
    i = 0 
    
    ## Iterar por cada 'elemento' del vector en cuestión
    while i < len(v):
        
        ## Concatenar la 'representación textual' del elemento actual
        resulting_string = resulting_string + str(v[i])
        
        ## Comprobar si 'no' es el *último* elemento
        if i < len(v) - 1:
            
            ## En tal caso, añadir un espacio tras el elemento
            resulting_string = resulting_string + " "
        
        ## Proceder con el 'siguiente' índice
        i = i + 1 
    
    ## Añadir el 'brakcet de cierre' a la cadena
    resulting_string = resulting_string + "]"  
    
    ## Se retorna la cadena formateada
    return resulting_string


## ******* Funciones complementarias para lectura de números *******

## Función para cargar una matriz 'partiendo de' un archivo *.txt*
def load_pattern_from_txt(filepath):
    
    ### Inicializar el vector plano que contendrá los *píxeles*
    flat_vector = []
    
    ## Intentar abrir el archivo en 'modo lectura' (*r*)
    try:
        with open(filepath, 'r') as f:
            for line in f:
                ## Eliminar 'espacios' & 'saltos de línea'; dividir el resultado por el *espacio*
                row_elements = [int(x) for x in line.strip().split() if x.isdigit()]
                
                ## Ignorar líneas vacías
                if not row_elements:
                    continue
                
                ## Verificar que la *fila* tenga el número correcto de *columnas*
                if len(row_elements) != MATRIX_COLS:
                    
                    ## Indica si un archivo tiene formato correcto o no
                    print(f"Alerta: Fila en {filepath} tiene {len(row_elements)} columnas -> se esperaban {MATRIX_COLS}")
                    continue
                
                ## Añadir los elementos de la *fila* al 'vector plano'
                flat_vector.extend(row_elements)
    
    ## Escepción en caso de que el archivo *no exista*
    except FileNotFoundError:
        print(f"Error! El archivo no fue encontrado en la dirección de archivo '{filepath}'")
        return None
    
    ## Crear variable de 'número de píxeles' leídos
    num_pixels = len(flat_vector)
        
    ## En caso que 'num_pixeles' no coincida con el esperado - error!
    if num_pixels != N_NEURONS:
        ## Mostrar mensaje de error
        print(f"Error: {filepath} tiene {len(flat_vector)} píxeles. Se esperaban {N_NEURONS}. Patrón inválido.")
        return None

    ## Convertir el 'vector plano' *[0, 1]* a 'bipolar' *[-1, 1]*
    bipolar_pattern = to_bipolar(flat_vector)
    return bipolar_pattern

## Funcion para cargar los archivos & retornar patrones para 'mapeo' de nombres
def load_all_training_patterns(folder_path):
    
    ## Inicializar la 'lista de patrones' & 'mapa de nombres'
    patterns_list = []
    name_map = {}
    
    # Listar todos los archivos en el directorio
    try:
        ## Leer todos los archivos *.txt* en la carpeta, escepto 'x.txt' (patrón de prueba)
        filenames = [f for f in os.listdir(folder_path) if f.endswith('.txt') and f != 'x.txt']
        
    ## Excepción en caso de que la carpeta *no exista*
    except FileNotFoundError:
        print(f"Error: Carpeta '{folder_path}' no encontrada. Asegúrate de descargarla.")
        return [], {}

    ## Indicar el número de patrones que se van a cargar
    print(f" *** Cargando {len(filenames)} patrones de entrenamiento  ***")
    
    ## Iterar por *cada* archivo en la carpeta de destino
    for i, filename in enumerate(filenames):
        ## Construir la 'ruta completa' del archivo
        filepath = os.path.join(folder_path, filename)
        
        ## Cargar el patrón desde el archivo *.txt*
        bipolar_pattern = load_pattern_from_txt(filepath)
        
        ## En caso que el patrón sea válido -> añadirlo a la 'lista de patrones'
        if bipolar_pattern:
            
            ## Añadir el patrón bipolar a la lista
            patterns_list.append(bipolar_pattern)
            
            ## El nombre del patrón es el nombre del archivo sin la extensión (.txt)
            pattern_name = filename.replace('.txt', '')
            name_map[i] = pattern_name 
            
            ## Indicar que el patrón fue cargado correctamente
            print(f"Patrón {i} ('{pattern_name}') cargado correctamente.")

    ## Retornar la 'lista de patrones' y el 'mapa de nombres'
    return patterns_list, name_map

## Función para mostrar la figura 'N x M' partiendo de un *vector plano bipolar*
def print_figure(v, rows=MATRIX_ROWS, cols=MATRIX_COLS):
    
    ## Corroborar que las dimensiones del vector son las esperadas
    if len(v) != rows * cols:
        
        ## Mostrar mensaje de error:
        print(f"Error! El vector es de dimensiones incorrectas ({len(v)}). Se esperaban '{rows * cols}'")
        return

    ## Mostrar la 'línea superior' de separación
    print("-" * (cols * 2 + 1))

    ## Iterar por *cada* fila
    for i in range(rows):
        
        ## Inicializar la 'cadena de caracteres' que contendrá la fila formateada
        row_str = ""
        
        ## Iterar por *cada* columna
        for j in range(cols):
            
            ## Calcular el 'índice' correspondiente en el vector plano
            indx = i * cols + j
            
            ## Mapear el *valor bipolar* a un 'caracter visual'
            char = '#' if v[indx] == 1 else ' ' 
            
            ## Añadir el caracter a la 'cadena de la fila'
            row_str += char + ' '
            
        ## Imprimir la *fila formateada*
        print(row_str)
    
    ## Imprimir la 'línea de separación' tras cada fila
    print("-" * (cols * 2 + 1))
    return


## ******** Ejecución principal del programa ********

## Carga los patrones de entrenamiento desde la carpeta 'datasets'
almacenamiento_patrones, nombres_patrones = load_all_training_patterns("datasets")

## Verificar si se realizó la 'carga de patrones'
if not almacenamiento_patrones:
    print("No se cargaron patrones de entrenamiento válidos.")
    
## En caso de que 'sí' se haya realizado
else:
    
    ## Definir la 'matriz de pesos' entrenada
    the_weight_matrix = build_weights(almacenamiento_patrones)
    print("\nMatriz de pesos entrenada con éxito.")

    ## Cargar el 'patrón de prueba' - archivo *x.txt*
    input_pattern = load_pattern_from_txt(TEST_FILE_PATH) 

    ## Verificar si se cargó el patrón de prueba
    if input_pattern:
        print(f"\nSe inicia la identificación del *patrón de prueba* -> {TEST_FILE_PATH}")

        ## Intentar la obtención del 'patrón orginal' de un input *ruidoso* - 20 epochs
        ## En caso de no lograrlo (converger), se retorna el 'último patrón logrado'
        recovered_pattern = recall_sync(the_weight_matrix, input_pattern, max_steps = 20)
        
        ## Clasificar el 'patrón recuperado' al *patrón almacenado* más cercano
        assigned_index = classify(recovered_pattern, almacenamiento_patrones)
        
        ## Mostrar los resultados
        print("\nPatrón recuperado por la red:")
        print_figure(recovered_pattern, MATRIX_ROWS, MATRIX_COLS) 
        
        ## Obtener el nombre del patrón identificado (si existe)
        nombre_identificado = nombres_patrones.get(assigned_index, "Patrón Desconocido/No-almacenado")

        ## Mostrar el 'resultado final' de la identificación
        print("\n *** Resultado de la Identificación  ***")
        print(f"El patrón de prueba se estabilizó en un estado que es más similar a:")
        print(f"Patrón {assigned_index}: '{nombre_identificado}'")
        
        ## Calcular la *distancia de Hamming*
        difs_al_patron = diferencias_por_posicion(recovered_pattern, almacenamiento_patrones[assigned_index])
        print(f"Distancia de Hamming al patrón almacenado: {difs_al_patron} píxeles diferentes.")
    
    ## En caso de que no se haya podido cargar el patrón de prueba
    else:
        print("No se pudo cargar el patrón de prueba 'x.txt'.")

## ******* Referencias *******
## Hopfield, J. J., & Tank, D. W. (1985). “Neural” computation of decisions in optimization problems. Biological Cybernetics. https://doi.org/10.1007/BF00339943
## Stanford HAI. (2024). From Brain to Machine: The Unexpected Journey of Neural Networks. Stanford HAI. https://hai.stanford.edu/news/brain-machine-unexpected-journey-neural-networks
## Roberts, E. (1999). Neural Networks - History. Stanford University. https://cs.stanford.edu/people/eroberts/courses/soco/projects/neural-networks/History/history2.html
## McKinsey & Company. (2018). Deep learning's origins and pioneers. McKinsey & Co. https://www.mckinsey.com/featured-insights/artificial-intelligence/deep-learnings-origins-and-pioneers
## Hopfield, J. J. (1982). Neural networks and physical systems with emergent collective computational abilities. Proceedings of the National Academy of Sciences, 79(8), 2558-2562. https://www.pnas.org/doi/10.1073/pnas.79.8.2554
## Niu, C., & Collaborators. (2024). A self-learning magnetic Hopfield neural network with intrinsic unsupervised learning. Scientific Reports. https://pmc.ncbi.nlm.nih.gov/articles/PMC11665918/
## MacKay, D. J. C. (2003). Information Theory, Inference and Learning Algorithms. Cambridge University Press. http://www.inference.org.uk/itprnn/book.pdf
## Niu, C., & Collaborators. (2024). A self-learning magnetic Hopfield neural network with intrinsic unsupervised learning. Scientific Reports. https://dl.acm.org/doi/10.5555/109230.109327
## Varela-Arregoces, E. (2020). Redes neuronales artificiales: Una revisión del estado actual. Revista Científica Universidad Simón Bolívar. https://revistas.unisimon.edu.co/index.php/identic/article/download/2455/2348
## Mendoza, N. J. (2023). La Red de Hopfield. Revista de Información, Tecnología y Sociedad. http://revistasbolivianas.umsa.bo/scielo.php?script=sci_arttext&pid=S199740442009000100009&lng=es&nrm=iso
## Batiuk, T. (2025). Enhancing image recognition patterns with Hopfield networks. Logos Science Proceedings. https://archive.logosscience.com/index.php/conference-proceedings/article/view/2728
## Abu-Mostafa, Y. S., & Jacques, J. M. (1985). Information capacity of the Hopfield model. IEEE Transactions on Information Theory, 31(4), 461–464. https://ieeexplore.ieee.org/document/1057069
