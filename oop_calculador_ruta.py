class Nodo:
    def __init__(self, padre=None, posicion=None):
        self.padre = padre
        self.posicion = posicion
        self.g = 0  # coste desde el inicio hasta este nodo
        self.h = 0  # estimación del coste desde este nodo hasta el objetivo
        self.f = 0  # coste total

class Mapa:
    def __init__(self, laberinto):
        self.laberinto = laberinto

    def es_valida(self, posicion):
        x, y = posicion
        if x < 0 or x >= len(self.laberinto) or y < 0 or y >= len(self.laberinto[0]):
            return False
        return self.laberinto[x][y] == 0
    
    def quitar_obstaculo(self, posicion):
        x, y = posicion
        if 0 <= x < len(self.laberinto) and 0 <= y < len(self.laberinto[0]):
            if self.laberinto[x][y] in [1, 2, 3]:  # Verificar si es un obstáculo
                self.laberinto[x][y] = 0  # Quitar el obstáculo
                print(f"Obstáculo en la posición {posicion} ha sido removido.")
                return True # se quito el obstaculo de forma exitosa
            else:
                print(f"No hay obstáculo en la posición {posicion} para quitar.")
                return False
        
            
        else:
            print("La posición dada está fuera del rango del laberinto.")
            return False
    

    def imprimir(self):
        for i, fila in enumerate(self.laberinto):
            for j, columna in enumerate(fila):
                if i == 0 or j == 0:
                    if j == 0:
                        print(f'\033[32m{columna}\033[0m  ', end=' ')
                    else:
                        print(f'\033[32m{columna}\033[0m', end=' ')
                    if i == 0 and j == 9:
                        print()
                elif columna == 1:
                    print(f'\033[31m{columna}\033[0m', end=' ')
                elif columna == '*':  # El * indica el recorrido elegido como el más óptimo, y lo imprime en amarillo
                    print(f'\033[33m{columna}\033[0m', end=' ')
                elif columna == 3:  # El 3 es un obstáculo más, se imprime en magenta
                    print(f'\033[34m{columna}\033[0m', end=' ')
                elif columna == 2:  # El 2 indica otro obstáculo, se imprime en celeste
                    print(f'\033[36m{columna}\033[0m', end=' ')
                elif columna == 'I' or columna == 'F':  # La I es el Inicio y la F es el final
                    print(f'\033[35m{columna}\033[0m', end=' ')
                else:
                    print(columna, end=' ')
            print()

class CalculadoraDeRutas:
    def __init__(self, mapa):
        self.mapa = mapa

    def A_estrella(self, inicio, fin):
        # Crear nodo inicial y nodo final
        nodo_inicio = Nodo(None, inicio)
        nodo_fin = Nodo(None, fin)

        # Inicializar lista open y closed
        open_list = []
        closed_list = []

        # Añadir el nodo inicial a la open_list
        open_list.append(nodo_inicio)

        # Bucle hasta encontrar el objetivo
        while open_list:
            # Obtener el nodo actual
            nodo_actual = open_list[0]
            indice_actual = 0
            for index, item in enumerate(open_list):
                if item.f < nodo_actual.f:
                    nodo_actual = item
                    indice_actual = index

            # Eliminar nodo actual de open_list y añadirlo a closed_list
            open_list.pop(indice_actual)
            closed_list.append(nodo_actual)

            # Verificar si se ha llegado al nodo objetivo
            if nodo_actual.posicion == nodo_fin.posicion:
                camino = []
                nodo_actual_temp = nodo_actual
                while nodo_actual_temp is not None:
                    camino.append(nodo_actual_temp.posicion)
                    nodo_actual_temp = nodo_actual_temp.padre
                return camino[::-1]  # Devolver el camino invertido

            # Generar nodos hijos
            hijos = []
            for nueva_posicion in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Vecinos
                # Obtener la posición del nodo
                posicion_nodo = (nodo_actual.posicion[0] + nueva_posicion[0], nodo_actual.posicion[1] + nueva_posicion[1])

                # Verificar si está dentro del laberinto y si no es un obstáculo
                if self.mapa.es_valida(posicion_nodo):
                    # Crear nuevo nodo
                    nuevo_nodo = Nodo(nodo_actual, posicion_nodo)
                    hijos.append(nuevo_nodo)

            # Loop a través de hijos
            for hijo in hijos:
                # Si el hijo está en closed_list, saltarlo
                if hijo in closed_list:
                    continue

                # Calcular f, g y h
                hijo.g = nodo_actual.g + 1
                hijo.h = ((hijo.posicion[0] - nodo_fin.posicion[0]) ** 2) + ((hijo.posicion[1] - nodo_fin.posicion[1]) ** 2)
                hijo.f = hijo.g + hijo.h

                #  Verifica si hay un nodo en open_list con la misma posición y un menor costo g que el nodo hijo, saltarlo
                if any(hijo.posicion == nodo_open.posicion and hijo.g > nodo_open.g for nodo_open in open_list):
                    continue

                # Añadir el hijo a open_list
                open_list.append(hijo)

def solicitar_coordenadas1(tipo, mapa):
    while True:
        coordenadas = tuple(map(int, input(f"Introduce las coordenadas de {tipo} (En este formato: x,y): ").split(",")))
        if mapa.es_valida(coordenadas):
            return coordenadas
        else:
            print(f"La coordenada de {tipo} no es válida, la coordenada ingresada ya está ocupada. Inténtalo de nuevo por favor.")

def solicitar_coordenadas2(tipo, mapa):
    while True:
        coordenadas = tuple(map(int, input(f"Introduce las coordenadas de {tipo} (En este formato: x,y): ").split(",")))
        if mapa.quitar_obstaculo(coordenadas):
            return coordenadas
        

# Crear el mapa
laberinto = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [2, 0, 0, 1, 0, 1, 0, 0, 0, 2],
    [3, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [4, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [5, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
    [6, 1, 0, 1, 0, 0, 1, 0, 1, 2],
    [7, 0, 2, 1, 0, 3, 0, 0, 0, 0],
    [8, 1, 0, 0, 0, 3, 0, 0, 2, 0],
    [9, 0, 1, 1, 0, 0, 0, 0, 0, 0]
]
mapa = Mapa(laberinto)

# Solicitar coordenada de inicio
inicio = solicitar_coordenadas1("inicio", mapa)
print(f"Coordenada de inicio aceptada: {inicio}")

# Solicitar coordenada de final
fin = solicitar_coordenadas1("fin", mapa)
print(f"Coordenada de fin aceptada: {fin}")

# Solicitar coordenada de obstáculo
obstaculo = solicitar_coordenadas1("obstáculo", mapa)
print(f"Coordenada de obstáculo aceptada: {obstaculo}")
laberinto[obstaculo[0]][obstaculo[1]] = 3


# Crear la calculadora de rutas
calculadora = CalculadoraDeRutas(mapa)

# Calcular el camino
camino = calculadora.A_estrella(inicio, fin)
print("Camino encontrado:", camino)

# Guardar camino
for x, y in camino:
    laberinto[x][y] = '*'

# Marcar el inicio y el fin en el laberinto
laberinto[inicio[0]][inicio[1]] = 'I'
laberinto[fin[0]][fin[1]] = 'F'

# Imprimir el mapa con el camino
mapa.imprimir()

# Solicitar coordenada de obstáculo a quitar
obstaculo_a_quitar = solicitar_coordenadas2("obstáculo a quitar", mapa)
laberinto[obstaculo[0]][obstaculo[1]] = 0

# Imprimir el mapa después de quitar el obstáculo
mapa.imprimir()