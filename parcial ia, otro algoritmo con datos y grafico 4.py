import json  # Librería para manejar datos en formato JSON
import networkx as nx  # Librería para trabajar con grafos
import matplotlib.pyplot as plt  # Librería para graficar los grafos

def cargar_grafo(datos):
    """
    Carga los datos en dos grafos dirigidos:
    - G_tiempo: usa los tiempos de viaje como peso.
    - G_distancia: usa la distancia en kilómetros como peso.
    """
    G_tiempo = nx.DiGraph()  # Grafo dirigido basado en el tiempo de viaje
    G_distancia = nx.DiGraph()  # Grafo dirigido basado en la distancia en km

    for origen, destinos in datos.items():  # Recorremos cada nodo origen
        for destino, valores in destinos.items():  # Revisamos los destinos conectados a ese origen
            G_tiempo.add_edge(origen, destino, weight=valores["tiempo"])  # Agregamos arista con peso de tiempo
            G_distancia.add_edge(origen, destino, weight=valores["distancia"])  # Agregamos arista con peso de distancia
    
    return G_tiempo, G_distancia  # Retornamos los dos grafos

def ruta_mas_rapida(G, inicio):
    """
    Calcula la ruta más rápida desde el nodo de inicio usando el algoritmo de Bellman-Ford.
    Devuelve el camino más corto desde el inicio a cada nodo y los tiempos totales.
    """
    try:
        distancias, _ = nx.single_source_bellman_ford(G, inicio, weight='weight')
        return distancias  # Retorna diccionario con las distancias mínimas
    except nx.NetworkXUnbounded:
        print("Error: el grafo contiene un ciclo negativo.")
        return None

def tsp_aproximado(G, inicio):
    """
    Usa la heurística de NetworkX para resolver el problema del viajero (*Traveling Salesman Problem*).
    Devuelve una ruta aproximada que visita todos los nodos y vuelve al inicio.
    """
    if nx.is_strongly_connected(G):  # Verifica si el grafo es fuertemente conectado
        return nx.approximation.traveling_salesman_problem(G, cycle=True, weight="weight")
    else:
        print("El grafo no es fuertemente conectado, convirtiéndolo en no dirigido...")
        G_undirected = G.to_undirected()  # Lo convertimos en un grafo no dirigido
        return nx.approximation.traveling_salesman_problem(G_undirected, cycle=True, weight="weight")

def graficar_ruta(G, ruta, titulo, color):
    """
    Grafica la ruta sobre el grafo.
    """
    plt.figure(figsize=(10, 7))

    # Posiciones geográficas aproximadas de los nodos (para mejor visualización)
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
    
    pos = {nodo: posiciones[nodo] for nodo in G.nodes if nodo in posiciones}
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=1500, font_size=9, edge_color="gray")
    
    # Dibujar la ruta específica
    path_edges = list(zip(ruta, ruta[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color=color, width=2.5, style="solid" if color == 'red' else "dashed")
    
    # Numerar los nodos en orden de visita
    for i, nodo in enumerate(ruta):
        plt.text(pos[nodo][0], pos[nodo][1] + 0.02, str(i + 1), fontsize=12, fontweight='bold', color=color)
    
    plt.title(titulo)
    plt.show()

# Datos de conexión entre los nodos (representados como un diccionario JSON)
json_data = '''
{
    "Universidad Sergio Arboleda": {
        "Parque Principal Soacha": {"tiempo": 40, "distancia": 24},
        "Parque Principal La Calera": {"tiempo": 32, "distancia": 18}
    },
    "Parque Principal Soacha": {
        "Parque Principal Villavicencio": {"tiempo": 167, "distancia": 114}
    },
    "Parque Principal Villavicencio": {
        "Parque Principal Tunja": {"tiempo": 260, "distancia": 262}
    },
    "Parque Principal Tunja": {
        "Parque Principal Toca": {"tiempo": 49, "distancia": 27}
    },
    "Parque Principal Toca": {
        "Parque Principal Cajica": {"tiempo": 143, "distancia": 139}
    },
    "Parque Principal Cajica": {
        "Parque Principal La Vega": {"tiempo": 83, "distancia": 75}
    },
    "Parque Principal La Vega": {
        "Parque Principal La Calera": {"tiempo": 113, "distancia": 83}
    },
    "Parque Principal La Calera": {
        "Universidad Sergio Arboleda": {"tiempo": 32, "distancia": 18}
    }
}
'''

# Cargar datos y construir los grafos
datos = json.loads(json_data)  # Convertimos el JSON a diccionario de Python
G_tiempo, G_distancia = cargar_grafo(datos)  # Creamos los grafos
inicio = "Universidad Sergio Arboleda"  # Nodo inicial

# Calcular la ruta más rápida usando Bellman-Ford
tiempos = ruta_mas_rapida(G_tiempo, inicio)
if tiempos:
    print(f"🔴 Ruta más rápida desde {inicio}:")
    for nodo, tiempo in tiempos.items():
        print(f"   {nodo} -> {tiempo} min")

# Calcular la mejor ruta usando heurística para TSP
ruta_optima = tsp_aproximado(G_distancia, inicio)
if ruta_optima:
    distancia_total = sum(G_distancia[ruta_optima[i]][ruta_optima[i+1]]["weight"] for i in range(len(ruta_optima)-1))
    print(f"\n🟢 Ruta más óptima (circuito más corto): {ruta_optima}")
    print(f"   Distancia total: {distancia_total} km")

# Graficar rutas
graficar_ruta(G_tiempo, list(tiempos.keys()), "Ruta más rápida (menor tiempo)", "red")
graficar_ruta(G_distancia, ruta_optima, "Ruta más óptima (menor distancia)", "green")
