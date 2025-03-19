import json  # Importamos la librería para manejar datos en formato JSON
import networkx as nx  # Importamos NetworkX para manejar grafos
from itertools import permutations  # Importamos permutations para probar todas las rutas en TSP
# ------------------------------
# Explicación del código:
# ------------------------------
# Este programa modela un sistema de rutas entre diferentes lugares y calcula la ruta más rápida y la más óptima.
#La hora de salida es a las 3:00 am. 
# Se utilizan dos grafos para representar las conexiones entre los destinos, uno basado en tiempo y otro en distancia.
# Se usa un grafo bidireccional con NetworkX para representar los destinos y sus conexiones.
# Se aplican algoritmos como Dijkstra y TSP para encontrar rutas eficientes.

# Función para cargar los datos del JSON y crear dos grafos (uno para tiempo y otro para distancia)
def cargar_grafo(datos):
    G_tiempo = nx.Graph()  # Grafo donde las aristas representan tiempo de viaje
    G_distancia = nx.Graph()  # Grafo donde las aristas representan distancia en km

    # Iteramos sobre los datos JSON
    for origen, destinos in datos.items():
        for destino, valores in destinos.items():
            # Agregamos conexiones entre nodos con sus respectivos pesos
            G_tiempo.add_edge(origen, destino, weight=valores["tiempo"])
            G_distancia.add_edge(origen, destino, weight=valores["distancia"])
    
    return G_tiempo, G_distancia  # Retornamos los dos grafos

# Algoritmo de Dijkstra para encontrar la ruta más rápida (menor tiempo)
def ruta_mas_rapida(G_tiempo, inicio, fin):
    # Encontramos el camino más corto en términos de tiempo
    ruta = nx.shortest_path(G_tiempo, source=inicio, target=fin, weight="weight")
    # Calculamos el tiempo total de la ruta óptima
    tiempo_total = nx.shortest_path_length(G_tiempo, source=inicio, target=fin, weight="weight")
    return ruta, tiempo_total  # Retornamos la ruta y el tiempo total

# Algoritmo de Dijkstra para encontrar la ruta más corta (menor distancia)
def ruta_mas_optima(G_distancia, inicio, fin):
    # Encontramos el camino más corto en términos de distancia
    ruta = nx.shortest_path(G_distancia, source=inicio, target=fin, weight="weight")
    # Calculamos la distancia total de la ruta óptima
    distancia_total = nx.shortest_path_length(G_distancia, source=inicio, target=fin, weight="weight")
    return ruta, distancia_total  # Retornamos la ruta y la distancia total

# Algoritmo de Fuerza Bruta para el Problema del Viajero (TSP)
def circuito_tsp(G, inicio):
    nodos = list(G.nodes())  # Obtenemos todos los nodos del grafo
    nodos.remove(inicio)  # Eliminamos el nodo de inicio de la lista de nodos a recorrer
    mejor_ruta = None  # Inicializamos la mejor ruta como None
    mejor_peso = float("inf")  # Inicializamos el mejor peso con infinito

    # Generamos todas las posibles permutaciones de los nodos
    for perm in permutations(nodos):
        ruta = [inicio] + list(perm) + [inicio]  # Construimos la ruta cerrada (circuito)
        
        try:
            # Calculamos el peso total de la ruta
            peso = sum(G[ruta[i]][ruta[i+1]]["weight"] for i in range(len(ruta) - 1))
        except KeyError:
            continue  # Si alguna conexión no existe, ignoramos esta ruta

        # Si encontramos una mejor ruta, la actualizamos
        if peso < mejor_peso:
            mejor_peso = peso
            mejor_ruta = ruta

    return mejor_ruta, mejor_peso  # Retornamos la mejor ruta y su peso

# Datos en formato JSON (Representan un mapa con tiempos y distancias entre destinos)
json_data = '''
{
    "Universidad Sergio Arboleda": {
        "Parque Principal Soacha": {"tiempo": 40, "distancia": 24},
        "Parque Principal La Calera": {"tiempo": 32, "distancia": 18}
    },
    "Parque Principal Soacha": {
        "Universidad Sergio Arboleda": {"tiempo": 40, "distancia": 24},
        "Parque Principal Villavicencio": {"tiempo": 167, "distancia": 114}
    },
    "Parque Principal Villavicencio": {
        "Parque Principal Soacha": {"tiempo": 167, "distancia": 114},
        "Parque Principal Tunja": {"tiempo": 260, "distancia": 262}
    },
    "Parque Principal Tunja": {
        "Parque Principal Villavicencio": {"tiempo": 260, "distancia": 262},
        "Parque Principal Toca": {"tiempo": 49, "distancia": 27}
    },
    "Parque Principal Toca": {
        "Parque Principal Tunja": {"tiempo": 49, "distancia": 27},
        "Parque Principal Cajica": {"tiempo": 143, "distancia": 139}
    },
    "Parque Principal Cajica": {
        "Parque Principal Toca": {"tiempo": 143, "distancia": 139},
        "Parque Principal La Vega": {"tiempo": 83, "distancia": 75}
    },
    "Parque Principal La Vega": {
        "Parque Principal Cajica": {"tiempo": 83, "distancia": 75},
        "Parque Principal La Calera": {"tiempo": 113, "distancia": 83}
    },
    "Parque Principal La Calera": {
        "Parque Principal La Vega": {"tiempo": 113, "distancia": 83},
        "Universidad Sergio Arboleda": {"tiempo": 32, "distancia": 18}
    }
}
'''

# Cargamos los datos JSON y creamos los grafos
datos = json.loads(json_data)
G_tiempo, G_distancia = cargar_grafo(datos)

inicio = "Universidad Sergio Arboleda"  # Definimos el punto de inicio del recorrido

# Calculamos la ruta más rápida (menor tiempo) usando TSP
ruta_rapida, tiempo_total = circuito_tsp(G_tiempo, inicio)

# Calculamos la ruta más óptima (menor distancia) usando TSP
ruta_optima, distancia_total = circuito_tsp(G_distancia, inicio)

# Mostramos los resultados obtenidos
print(f"🔴 Ruta más rápida (menor tiempo): {ruta_rapida}, Tiempo total: {tiempo_total} min")
print(f"🟢 Ruta más óptima (menor distancia): {ruta_optima}, Distancia total: {distancia_total} km")
