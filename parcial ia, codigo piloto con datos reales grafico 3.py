import json  # Importamos el módulo json para cargar y manejar datos en formato JSON
import networkx as nx  # Importamos NetworkX para manejar grafos
import matplotlib.pyplot as plt  # Importamos Matplotlib para graficar los resultados

# Función para cargar datos JSON y construir dos grafos: uno para tiempo y otro para distancia
def cargar_grafo(datos):
    G_tiempo = nx.Graph()  # Grafo para el tiempo de viaje entre lugares
    G_distancia = nx.Graph()  # Grafo para la distancia en kilómetros entre lugares

    # Recorremos los datos del JSON y agregamos las conexiones a los grafos
    for origen, destinos in datos.items():
        for destino, valores in destinos.items():
            G_tiempo.add_edge(origen, destino, weight=valores["tiempo"])  # Usamos el tiempo como peso en G_tiempo
            G_distancia.add_edge(origen, destino, weight=valores["distancia"])  # Usamos la distancia como peso en G_distancia
    
    return G_tiempo, G_distancia  # Retornamos ambos grafos

# Función que implementa el algoritmo del Viajante de Comercio (TSP) usando fuerza bruta
def circuito_tsp(G, inicio):
    from itertools import permutations  # Importamos permutations para generar todas las posibles rutas
    
    nodos = list(G.nodes())  # Lista de todos los nodos en el grafo
    nodos.remove(inicio)  # Eliminamos el nodo inicial para permutar solo los demás nodos
    mejor_ruta = None  # Guardará la mejor ruta encontrada
    mejor_peso = float("inf")  # Inicializamos el mejor peso con infinito (queremos minimizarlo)

    # Generamos todas las posibles rutas comenzando y terminando en el nodo de inicio
    for perm in permutations(nodos):
        ruta = [inicio] + list(perm) + [inicio]  # La ruta siempre comienza y termina en "inicio"

        try:
            # Calculamos el peso total de la ruta sumando los pesos de cada conexión
            peso = sum(G[ruta[i]][ruta[i+1]]["weight"] for i in range(len(ruta) - 1))
        except KeyError:
            continue  # Si una ruta no tiene conexión entre algunos nodos, la ignoramos
        
        # Si encontramos una ruta con menor peso, la guardamos como la mejor hasta ahora
        if peso < mejor_peso:
            mejor_peso = peso
            mejor_ruta = ruta

    return mejor_ruta, mejor_peso  # Retornamos la mejor ruta y su peso

# Función para graficar una ruta en un mapa
def graficar_ruta(G, ruta, titulo, color):
    plt.figure(figsize=(10, 7))  # Configuramos el tamaño de la gráfica
    
    # Definimos posiciones aproximadas de los lugares en coordenadas ficticias
    posiciones = {
        "Universidad Sergio Arboleda": (4.6584, -74.0937),
        "Parque Principal Soacha": (4.5773, -74.2144),
        "Parque Principal Villavicencio": (4.1420, -73.6266),
        "Parque Principal Tunja": (5.5353, -73.3672),
        "Parque Principal Toca": (5.5646, -73.1818),
        "Parque Principal Cajica": (4.9226, -74.0273),
        "Parque Principal La Vega": (5.0101, -74.3445),
        "Parque Principal La Calera": (4.6926, -73.9630)
    }
    
    pos = {nodo: posiciones[nodo] for nodo in G.nodes if nodo in posiciones}  # Extraemos posiciones de los nodos en el grafo
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=1500, font_size=9, edge_color="gray")  # Dibujamos el grafo
    
    # Dibujamos la ruta óptima resaltada en el color especificado
    path_edges = list(zip(ruta, ruta[1:]))  # Obtenemos los pares de conexiones en la ruta
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color=color, width=2.5, style="solid" if color == 'red' else "dashed")

    # Agregamos números en los nodos para indicar el orden de visita
    for i, nodo in enumerate(ruta):
        plt.text(pos[nodo][0], pos[nodo][1] + 0.02, str(i + 1), fontsize=12, fontweight='bold', color=color)
    
    plt.title(titulo)  # Agregamos un título al gráfico
    plt.show()  # Mostramos el gráfico

# Datos en formato JSON que representan los lugares y sus conexiones con tiempos y distancias
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

# Cargar datos desde el JSON y crear los grafos de tiempo y distancia
datos = json.loads(json_data)
G_tiempo, G_distancia = cargar_grafo(datos)

# Definimos el punto de inicio del recorrido
inicio = "Universidad Sergio Arboleda"

# Calculamos la ruta más rápida (menor tiempo) usando TSP
ruta_rapida, tiempo_total = circuito_tsp(G_tiempo, inicio)

# Calculamos la ruta más óptima (menor distancia) usando TSP
ruta_optima, distancia_total = circuito_tsp(G_distancia, inicio)

# Imprimimos los resultados
print(f"🔴 Ruta más rápida (menor tiempo): {ruta_rapida}, Tiempo total: {tiempo_total} min")
print(f"🟢 Ruta más óptima (menor distancia): {ruta_optima}, Distancia total: {distancia_total} km")

# Graficamos las rutas obtenidas
graficar_ruta(G_tiempo, ruta_rapida, "Ruta más rápida (menor tiempo)", "red")
graficar_ruta(G_distancia, ruta_optima, "Ruta más óptima (menor distancia)", "green")
