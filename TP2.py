import random
import numpy as np
import Agente as ag
import Grafo as grafo
import DSUGroups as dsu
import Simulacion2 as sim

import matplotlib.pyplot as plt



    
    
cantidad_agentes = 100
proporcion_afectados = 0.5
densidad_grafo = 0.5
costo_transaccion = 0
submultiplicador_afectados = 500
multiplicador_de_coordinacion = 0.0004
multiplicador_de_utilidad = 1000
contaminacion_maxima = 100
modo_informacion=True
cantidad_de_ticks= 300


mi_simulacion = sim.Simulacion()    

mi_simulacion.simular(cantidad_agentes, proporcion_afectados, densidad_grafo, costo_transaccion, submultiplicador_afectados, multiplicador_de_coordinacion, multiplicador_de_utilidad, contaminacion_maxima, modo_informacion, cantidad_de_ticks)
libro1=mi_simulacion.sacar_libro()
mi_simulacion.finalizar_simulacion()


seq_contaminacion = sim.seq_contaminacion
seq_cantidad_grupos = sim.seq_cantidad_grupos
seq_cantidad_ofertas = sim.seq_cantidad_ofertas

# Setting up the plot
plt.figure(figsize=(10, 5))
plt.plot(seq_contaminacion, label='Contaminación', marker='o')
plt.plot(seq_cantidad_grupos, label='Cantidad de Grupos', marker='x')
plt.plot(seq_cantidad_ofertas, label='cantidad de ofertas',marker='x')

# Adding titles and labels
plt.title('Simulation Data Over Time')
plt.xlabel('Ticks')
plt.ylabel('Values')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

