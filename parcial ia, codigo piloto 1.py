"""
Este programa busca la ruta más óptima para visitar una serie de destinos,
usando el algoritmo del viajante (TSP - Traveling Salesman Problem) con fuerza bruta.
También grafica la ruta en un mapa de nodos y conexiones. Cabe aclarar que este fue 
un código de prueba para entender como funcionaban las variables y no utiliza datos reales.  

¿Por qué se eligió este enfoque?
- Se usa fuerza bruta porque la cantidad de destinos es pequeña.
- Se utiliza NetworkX para manejar grafos y matplotlib para visualización.
- Se implementa una estructura de datos clara con nodos y conexiones.

Variables principales:
- G: Grafo que representa los destinos y sus conexiones.
- destinos: Lista de lugares que forman los nodos del grafo.
- conexiones: Diccionario que almacena las rutas entre destinos con su tiempo asociado.
- inicio: Nodo desde donde comienza y termina el recorrido.
- mejor_ruta: Almacena la mejor ruta encontrada.
- mejor_distancia: Guarda la menor distancia calculada.
"""

import networkx as nx  # Librería para trabajar con grafos
import matplotlib.pyplot as plt  # Para graficar el grafo
from itertools import permutations  # Para generar todas las permutaciones posibles de rutas

def crear_grafo():
    """
    Crea y retorna un grafo con los destinos como nodos y sus conexiones con tiempos de viaje como aristas.
    """
    G = nx.Graph()  # Se crea un grafo no dirigido
    
    # Lista de destinos (nodos del grafo)
    destinos = [
        "Universidad Sergio Arboleda", "Parque Central Cajicá", "Parque Central Villavicencio", 
        "Parque Central Soacha", "Parque Central Tunja", "Parque Central Toca, Boyacá", 
        "Parque Central La Vega", "Parque Central La Calera"
    ]
    
    # Agregar nodos al grafo
    for destino in destinos:
        G.add_node(destino)
    
    # Diccionario con conexiones entre destinos y sus tiempos de viaje
    conexiones = {
        ("Universidad Sergio Arboleda", "Parque Central Cajicá"): 1.2,
        ("Parque Central Cajicá", "Parque Central Tunja"): 2.0,
        ("Parque Central Tunja", "Parque Central Toca, Boyacá"): 0.8,
        ("Parque Central Tunja", "Parque Central Villavicencio"): 3.5,
        ("Parque Central Villavicencio", "Parque Central Soacha"): 2.5,
        ("Parque Central Soacha", "Parque Central La Vega"): 1.5,
        ("Parque Central La Vega", "Parque Central La Calera"): 1.8,
        ("Parque Central La Calera", "Universidad Sergio Arboleda"): 1.0,
    }
    
    # Agregar conexiones (aristas) al grafo con su respectivo peso (tiempo de viaje)
    for (origen, destino), tiempo in conexiones.items():
        G.add_edge(origen, destino, weight=tiempo)
    
    return G

def ruta_mas_optima_tsp(G, inicio):
    """
    Encuentra la ruta más corta que visita todos los nodos y regresa al punto de inicio.
    Se basa en una búsqueda de fuerza bruta usando permutaciones.
    """
    nodos = list(G.nodes())  # Obtener todos los nodos del grafo
    nodos.remove(inicio)  # Excluir el nodo de inicio para generar rutas
    mejor_ruta = None  # Variable para almacenar la mejor ruta
    mejor_distancia = float('inf')  # Variable para almacenar la menor distancia encontrada
    
    # Generar todas las posibles rutas (permutaciones de los nodos)
    for perm in permutations(nodos):
        ruta = [inicio] + list(perm) + [inicio]  # Ruta que comienza y termina en 'inicio'
        distancia = 0  # Distancia acumulada en la ruta
        ruta_valida = True  # Bandera para verificar si la ruta es válida
        
        # Calcular la distancia total de la ruta
        for i in range(len(ruta) - 1):
            if G.has_edge(ruta[i], ruta[i+1]):  # Verificar si hay conexión entre nodos
                distancia += G[ruta[i]][ruta[i+1]]['weight']
            else:
                ruta_valida = False  # Si no hay conexión, descartar esta ruta
                break  # Salir del bucle
        
        # Si la ruta es válida y su distancia es menor que la mejor registrada, actualizar
        if ruta_valida and distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_ruta = ruta
    
    return mejor_ruta, mejor_distancia if mejor_ruta else ([], float('inf'))

def graficar_grafo(G, ruta_tsp=None):
    """
    Dibuja el grafo con los destinos y sus conexiones, resaltando la ruta óptima si está disponible.
    """
    pos = nx.spring_layout(G, seed=42)  # Generar una disposición de nodos
    plt.figure(figsize=(10, 7))  # Tamaño de la figura
    
    # Dibujar el grafo con nodos y conexiones
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=9, edge_color="gray")
    
    # Etiquetas de los pesos de las aristas (tiempo de viaje)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
    
    # Si se proporciona una ruta óptima, resaltarla en rojo
    if ruta_tsp:
        path_edges = list(zip(ruta_tsp, ruta_tsp[1:]))  # Crear pares de nodos consecutivos en la ruta
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2.5)
    
    plt.title("Mapa de Rutas")  # Título del gráfico
    plt.show()  # Mostrar el gráfico

# Crear el grafo
G = crear_grafo()

# Definir el nodo de inicio y calcular la mejor ruta TSP
inicio = "Universidad Sergio Arboleda"
tsp_ruta, tsp_distancia = ruta_mas_optima_tsp(G, inicio)

# Imprimir la mejor ruta encontrada y su distancia total
print(f"Ruta más óptima visitando todos los destinos (TSP): {tsp_ruta}, distancia total: {tsp_distancia} horas")

# Graficar el grafo con la ruta óptima
graficar_grafo(G, tsp_ruta)



