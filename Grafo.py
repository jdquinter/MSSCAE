
#Corregido x santi abajo deje comentado lo q estaba antes
import random
import heapq
import numpy as np



def f(x):
    return 1-(np.exp(3*x)-1)/(np.exp(3)-1)

def f_costo_arista(p_coordinacion):
    return f(random.random())*p_coordinacion



class Grafo:
    def __init__(self):
        self.adyacencias = []  
        self.generado = False    
    
            
        
    # Funcion que crea las aristas del grafo de manera aleatoria y posteriormente lo crea y lo devuelve
    def generador_grafo(self, densidad_conexion, param_transaccion, cant_agentes):
        if(self.generado is not False):
            raise ValueError("Ya se genero un grafo")

        # Definicion de aristas
        cantidad_de_aristas = int((cant_agentes - 1)*(1-densidad_conexion) + densidad_conexion*cant_agentes*(cant_agentes-1)*1/2)
        pares_de_adyacencias = []
        for i in range(cantidad_de_aristas):
            repeated=True
            while repeated:
                repeated = False
                a= random.randint(0, cant_agentes-1)
                b= random.randint(0, cant_agentes-1)
                if(a is not b):
                    t1=(a,b)
                    t2=(b,a)
                    for pair in pares_de_adyacencias:
                        if pair == t1 or pair == t2:
                            repeated=True
            pares_de_adyacencias.append((a,b))
            cantidad_de_aristas -= 1

        # Definicion de costos y lista de adyacencia
        lista_de_adyaciencia = [[] for _ in range(cant_agentes)]

        for pair in pares_de_adyacencias:
            costo= f_costo_arista(param_transaccion)
            a, b= pair
            lista_de_adyaciencia[a].append((b, costo))
            lista_de_adyaciencia[b].append((a, costo))
            
        # Inicializacion y return del grafo
        self.adyacencias= lista_de_adyaciencia
        self.generado=True



    def lista_caminos_minimos(self, start):
        distances=[0]
        for i in range(len(self.adyacencias)-1):
            distances.append(float('infinity'))
        queue = [(0, start)]
        while queue:
            current_distance, current_vertex = heapq.heappop(queue)
            if current_distance > distances[current_vertex]:
                continue
            for neighbor, weight in self.adyacencias[current_vertex]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))
        return distances


"""import random
import heapq
import numpy as np


import random

def f(x):
    return 1-(np.exp(3*x)-1)/(np.exp(3)-1)

def f_costo_arista(p_coordinacion):
    return f(random.random())*p_coordinacion



class Grafo:
    def __init__(self):
        self.adyacencias = []  
        self.generado = False    
    
            
        
    # Funcion que crea las aristas del grafo de manera aleatoria y posteriormente lo crea y lo devuelve
    def generador_grafo(self, densidad_conexion, param_transaccion, cant_agentes):
        if(self.generado is not False):
            raise ValueError("Ya se genero un grafo")

        # Definicion de aristas
        cantidad_de_aristas = int((cant_agentes - 1)*(1-densidad_conexion) + densidad_conexion*cant_agentes*(cant_agentes-1)*1/2)
        pares_de_adyacencias = []
        for i in range(cantidad_de_aristas):
            repeated=False #ciclo sin fin
            while not repeated:
                a= random.randint(0, cant_agentes)
                b= random.randint(0, cant_agentes)
                if(a is not b):
                    t1=(a,b)
                    t2=(b,a)
                    for pair in pares_de_adyacencias:
                        if pair == t1 or pair == t2:
                            repeated=True
                            #No agrega los pares a pares_de_adyacencias
            cantidad_de_aristas -= 1

        # Definicion de costos y lista de adyacencia
        lista_de_adyaciencia = [] #por como escribiste, tiene q ser un array de tamaño cant_agentes sino da error index
        for i in range(cant_agentes):
            lista_de_adyaciencia.append([])
        
        for pair in pares_de_adyacencias:
            costo= f_costo_arista(param_transaccion)
            a, b= pair
            lista_de_adyaciencia[a].append((b, costo))
            lista_de_adyaciencia[b].append((a, costo))
            
        # Inicializacion y return del grafo
        self.adyacencias= lista_de_adyaciencia
        self.generado=True



    def lista_caminos_minimos(self, start):
        distances=[0]
        for i in range(self.adyacencias.size()-1):
            distances.append(float('infinity'))
        queue = [(0, start)]
        while queue:
            current_distance, current_vertex = heapq.heappop(queue)
            if current_distance > distances[current_vertex]:
                continue
            for neighbor, weight in self.graph[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))
        return distances
            
"""