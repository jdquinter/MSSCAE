import random
import numpy as np
import Agente as ag
import Grafo as grafo
import DSUGroups as dsu
import Simulacion2 as sim
import matplotlib.pyplot as plt
from matplotlib import animation
import pandas as pd
import networkx as nx
import pandas as pd
import heapq as hp
import copy 
from matplotlib.animation import FuncAnimation


def cantidad_grupos(libro):
    lista_cantidad_grupos_por_tick = []
    for lista_padres in [row[2] for row in libro]:
        lista_padres.sort()
        cantidad_grupos = 1
        for i in range(1,len(lista_padres)):
            padre = lista_padres[i]
            if padre != lista_padres[i-1]:
                cantidad_grupos += 1
        lista_cantidad_grupos_por_tick.append(cantidad_grupos)
    return lista_cantidad_grupos_por_tick

def contaminaciones(libro):
    return [row[3] for row in libro]

def ofertas_aceptadas(libro):
    return [row[1] for row in libro]

def ofertas_general(libro):
    return [row[0] for row in libro]

def cantidad_ofertas(libro):
    return [len(row[0]) for row in libro]
    
def utilidad_ofertas_aceptadas(libro,lista_de_agentes):
    lista_utilidades_aceptadas =[]
    for lista_ofertas_aceptadas in [row[1] for row in libro]:
        utilidades_generadores = 0
        contaminacion = 0
        for oferta in lista_ofertas_aceptadas:
            agente = lista_de_agentes[oferta[2]]
            if agente.tipo == 'generador':
                utilidades_generadores+=agente.tabla_de_utilidad[oferta[0]]
                contaminacion += oferta[0]
        utilidades_afectados = 0
        for agente in lista_de_agentes:
            if agente.tipo == 'afectado':
                utilidades_afectados += agente.tabla_de_utilidad[contaminacion]

        lista_utilidades_aceptadas.append(utilidades_generadores + utilidades_afectados)
    return lista_utilidades_aceptadas

#No es util
def armar_grupos(libro):
    lista_de_padres = [row[2] for row in libro]
    grupos_integrantes = []
    for tick in range(len(lista_de_padres)):
        lista_de_padres_tick = lista_de_padres[tick]
        grupos = [[] for i in range(len(lista_de_padres_tick))]
        for nodo in lista_de_padres_tick:
            nodo_original = nodo
            while(lista_de_padres_tick[nodo]!=nodo):
                nodo = lista_de_padres_tick[nodo]
            print(nodo_original)
            grupos[nodo].append(nodo_original)

        grupos_integrantes.append(grupos)
    return grupos_integrantes

#No es util
def utilidades_individuales(libro, lista_de_agentes):
    
    
    contaminaciones_tick = contaminaciones(libro)
    ofertas_aceptad = ofertas_aceptadas(libro)
    utilidades_por_Agente = []
    grupos = armar_grupos(libro)
    listas_de_padres = [row[2] for row in libro]

    for i in range(len(ofertas_aceptad)):
        ofertas = ofertas_aceptad[i]
        for oferta in ofertas:
            agente = lista_de_agentes[oferta[2]]
            utilidades_por_agente_tick = [0]*len(lista_de_agentes)
            if agente.tipo == 'generador':
                utilidades_por_agente_tick[oferta[2]] = agente.tabla_de_utilidad[oferta[0]]
            if agente.tipo == 'afectado':
                padre = listas_de_padres[i][oferta[2]]
                grupo =  grupos[i][padre]
                for idintegrante in grupo:
                    utilidad = oferta[1]*oferta[3]
                    agente = lista_de_agentes[idintegrante]
                    utilidades_por_agente_tick[idintegrante]=utilidad
        utilidades_por_Agente.append(utilidades_por_agente_tick)
    
    return utilidades_por_Agente

def contaminacion_ofertas_aceptadas(libro):
    
    lista_contaminacion =[]
    for lista_ofertas_aceptadas in [row[1] for row in libro]:
        contaminacion = 0
        for row in lista_ofertas_aceptadas:
            if row[0] > 0:
                contaminacion += row[0]
        lista_contaminacion.append(contaminacion)
    return lista_contaminacion

def ofertas_afectados(libro):
    ofertas_afectados = []
    for ofertas in [row[1] for row in libro]:
        ofertas_afectados_tick = []
        for oferta in ofertas:
            if oferta[0]<0:
                ofertas_afectados_tick.append(oferta)
        ofertas_afectados.append(ofertas_afectados_tick)
    return ofertas_afectados

def ofertas_generadores(libro):
    ofertas_generadores = []
    for ofertas in [row[1] for row in libro]:
        ofertas_generadores_tick = []
        for oferta in ofertas:
            if oferta[0]>0:
                ofertas_generadores_tick.append(oferta)
        ofertas_generadores.append(ofertas_generadores_tick)
    return  ofertas_generadores

def derechos_adquiridos_afectados(libro):
    derechos_afectados = []
    for ofertas in [row[1] for row in libro]:
        derechos_adquiridos_afectados_tick = []
        for oferta in ofertas:
            if oferta[0]<0:
                derechos_adquiridos_afectados_tick.append(oferta[0])
        derechos_afectados.append(abs(sum(derechos_adquiridos_afectados_tick)))
    return derechos_afectados

def derechos_adquiridos_generadores(libro):
    derechos_generadores = []
    for ofertas in [row[1] for row in libro]:
        derechos_adquiridos_generadores_tick = []
        for oferta in ofertas:
            if oferta[0]>=0:
                derechos_adquiridos_generadores_tick.append(abs(oferta[0]))
        derechos_generadores.append(sum(derechos_adquiridos_generadores_tick))
    return derechos_generadores

def ofertas_afectados_sin_aceptar(libro):
    ofertas_afectados = []
    for ofertas in [row[0] for row in libro]:
        ofertas_afectados_tick = []
        for oferta in ofertas:
            if oferta[0]<0:
                ofertas_afectados_tick.append(oferta)
        ofertas_afectados.append(ofertas_afectados_tick)
    return ofertas_afectados

def ofertas_generadores_sin_aceptar(libro):
    ofertas_generadores = []
    for ofertas in [row[0] for row in libro]:
        ofertas_generadores_tick = []
        for oferta in ofertas:
            if oferta[0]>0:
                ofertas_generadores_tick.append(oferta)
        ofertas_generadores.append(ofertas_generadores_tick)
    return ofertas_generadores


def sum_nth_elements(list_of_lists):
    # Initialize the result list with 101 zeros
    result = [0] * 101
    
    # Loop through each inner list
    for inner_list in list_of_lists:
        # Loop through each element in the inner list
        for i in range(101):
            result[i] += inner_list[i]
    
    return result

def index_of_max_element(input_list):
    if not input_list:
        raise ValueError("The list is empty")
    max_index = 0
    max_value = input_list[0]
    
    for index, value in enumerate(input_list):
        if value > max_value:
            max_value = value
            max_index = index
            
    return max_index

def calcular_max(lista_de_agentes):
    
    tablas_afectados = []
    tablas_generadores = []
    for agente in lista_de_agentes:
        if agente.tipo == "afectado":
            tablas_afectados.append(agente.tabla_de_utilidad)
        if agente.tipo == "generador":
            tablas_generadores.append(agente.tabla_de_utilidad)
    
    # Lleno el heap con las utilidades de los generadores
    # heap con elementos de la forma (-utilidad,posicion)
    max_heap = []
    for tabla in tablas_generadores:
            hp.heappush(max_heap,(-tabla[0], 0))
            for posicion in range(1,101):
                utilidad = tabla[posicion] - tabla[posicion-1]
                hp.heappush(max_heap, (-utilidad, posicion))

    # Calculo la funcion de utilidad conjunta de los afectados
    tabla_conjunta = sum_nth_elements(tablas_afectados)
    
    # Calculo utilidades optimas de los generadores para cada cantidad de derechos 
    # Para que esto funcione se tiene que cumplir que nunca la utilidad para un generador en t[i] es mayor a la de t[i-1]
    optimos_generadores = []
    track = []
    optimos_generadores.append(0.0)
    for cant_derechos_generadores in range(1,101):
        temp = hp.heappop(max_heap)
        maximo = (-temp[0],temp[1]) 
        track.append(maximo)
        if optimos_generadores == []:
            optimos_generadores.append(maximo[0])
        else:
            optimos_generadores.append(maximo[0] + optimos_generadores[cant_derechos_generadores-1])
    
    # Calculo optimos parciales teniendo en cuenta generadores y afectados
    optimos_parciales = []
    for i, util_generadores in enumerate(optimos_generadores):
        optimos_parciales.append(tabla_conjunta[i]+util_generadores)
        
    
    optimo_contaminacion = index_of_max_element(optimos_parciales)
    optimo_util_total = optimos_parciales[optimo_contaminacion]
    optimo_util_afectados = tabla_conjunta[optimo_contaminacion]
    optimo_util_generadores = optimos_generadores[optimo_contaminacion]
    
    return (optimo_contaminacion, optimo_util_total, optimo_util_afectados, optimo_util_generadores)


############ Graficos #############################


def graficar_derechos_para_distintos_costos_de_transaccion(derechos_adquiridos_generadores,derechos_adquiridos_afectados):

    fig, axs = plt.subplots(2, 2, figsize=(10,12))
    ticks = range(200)
    axs[0,0].set_title('Costo de transaccion 0')
    axs[0,0].set_xlabel('tick')
    axs[0,0].set_ylabel('Derechos')
    axs[0,1].set_title('Costo de transaccion 100')
    axs[0,1].set_xlabel('tick')
    axs[0,1].set_ylabel('Derechos')
    axs[1,0].set_title('Costo de transaccion 300')
    axs[1,0].set_xlabel('tick')
    axs[1,0].set_ylabel('Derechos')
    axs[1,1].set_title('Costo de transaccion 1000')
    axs[1,1].set_xlabel('tick')
    axs[1,1].set_ylabel('Derechos')

    fontgeneradores = {
            'color':  'blue',
            'weight': 'normal',
            'size': 16,
            }
    fontafectados = {
            'color':  'red',
            'weight': 'normal',
            'size': 16,
            }

    cont = 0
    for j in [(0, 0),(0, 1),(1, 0),(1, 1)]:
        maximos_utilidades_generadores = 0
        maximos_utilidades_afectados = 0
        for i in range(5):
            axs[j[0],j[1]].plot(ticks, derechos_adquiridos_generadores[cont][i], color = 'blue',linewidth=0.5, alpha = 0.7)
            axs[j[0],j[1]].plot(ticks, derechos_adquiridos_afectados[cont][i], color ='red',linewidth=0.5, alpha = 0.7)
        cont += 1
    fig.text(0.1, 0.93, r'$Derechos\ de\ Generadores$', fontdict=fontgeneradores)
    fig.text(0.1, 0.95, r'$Derechos\ de\ Afectados$', fontdict=fontafectados)
    plt.show()
    
    
def grafica_grafo(nombre, coef, libro,lista_agentes):
    def update_linechart(t):

        lista_de_padres = [row[2] for row in libro]
        contaminacion = [row[3] for row in libro]
        derechos_adq_afc = derechos_adquiridos_afectados(libro)
        derechos_adq_gen = derechos_adquiridos_generadores(libro)
        

        fin = [lista_de_padres[t][i] for i in np.arange(0,len(lista_de_padres[0]))]
        for i in range(len(fin)):
            if fin[i] == i:
                fin[i] = 0
        conexiones = pd.DataFrame(
            {
            "inicio": np.arange(0,len(lista_de_padres[0])),
            "fin" : fin,
            }
        )
        colores = ['black'] 
        for i in range(1,len(lista_agentes)):
            if lista_agentes[i].tipo=='afectado':
                colores.append('blue')
            elif lista_agentes[i].tipo == 'generador':
                colores.append('red')

        options = {"node_color": colores, "node_size": 50, "linewidths": 0, "width": 0.3}
        ax.clear()
        G = nx.from_pandas_edgelist(conexiones, source="inicio", target="fin")



        center_node = 0
        edge_nodes = set(G) - {center_node}
        pos = nx.circular_layout(G.subgraph(edge_nodes))
        pos[center_node] = np.array([0, 0])
        edge_labels = nx.get_edge_attributes(G, "weight")

        nx.draw(G,pos, ax=ax,**options)
        ax.text(0.85,1.10,f'Coef. Cord:{coef}')
        ax.text(0.85,1.10,f'Coef. Cord:{coef}')
        ax.text(0.85,0.95,f'Tick:{t}')
        ax.text(0.85,0.9,f'Contaminacion:{contaminacion[t]}')
        ax.text(0.85,0.85,f'Derechos Generadores: {derechos_adq_gen[t]}')
        ax.text(0.85,0.8,f'Derechos Afectados: {derechos_adq_afc[t]}')

    fig, ax = plt.subplots(figsize=(10,10))
    num_frames = len([row[2] for row in libro])
    anim = animation.FuncAnimation(fig, update_linechart, frames = num_frames)
    anim.save(nombre)

def grafico_contaminacion_grupos_ofertas(libro):
    seq_contaminacion = contaminaciones(libro)
    seq_cantidad_grupos = cantidad_grupos(libro)
    seq_cantidad_ofertas = cantidad_ofertas(libro)

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

def grafico_utilidades_individuales(libro, lista_de_agentes):
    utilidades = utilidades_individuales(libro,lista_de_agentes)
    fig, ax = plt.subplots(figsize=(10,10))
    def update(frame):
        ax.clear()  # Limpiar el eje antes de dibujar el nuevo histograma
        #ax.set_xlim(-4, 4)  # Ajustar límites del eje x según los datos
        #ax.set_ylim(0, 300)  # Ajustar límites del eje y según los datos
        ax.set_title('Histograma en el Tiempo {}'.format(frame))
        ax.set_xlabel('Valor')
        ax.set_ylabel('Frecuencia')
        
        # Dibujar el histograma para el frame actual
        ax.bar(range(0,len(lista_de_agentes)),utilidades[frame], edgecolor='black')
        
        plt.show()
    # Crear la animación utilizando FuncAnimation
    animacion = FuncAnimation(fig, update, frames=len(utilidades), repeat=False)
    animacion.save('utilidades_individuales.gif')

def graficar_maximos(libros,lista_agentes):
    contaminacion = []
    utilidades_tot_maxima = []
    utilidades_generadores_max = []
    utilidades_afectados_max= []

    for libro in libros:
        lista_agentes = libro[1]
        cantidad_maxima = calcular_max(lista_agentes)
        contaminacion.append(cantidad_maxima[0])
        utilidades_tot_maxima.append(cantidad_maxima[1])
        utilidades_generadores_max.append(cantidad_maxima[3])
        utilidades_afectados_max.append(cantidad_maxima[2])
        contaminacion_simulacion.append(contaminacion_ofertas_aceptadas(libro[0])[-1])
        utilidades_tot_maxima_simulacion.append(utilidad_ofertas_aceptadas(libro[0],lista_agentes)[-1])


    fig, axs = plt.subplots(1,2)
    fig.set_figheight(6)
    fig.set_figwidth(10)


    axs[0].set_title("Utilidad maxima por submultiplicador")
    axs[0].set_xlabel("submultiplicador")
    axs[0].set_ylabel("utilidad")

    axs[0].plot(conjunto_submultiplicadores, utilidades_afectados_max, color = 'red', alpha = 0.5,linestyle = 'dotted', label = 'abs(Utilidad afectados)')
    axs[0].plot(conjunto_submultiplicadores, utilidades_generadores_max,color = 'blue', alpha = 0.5,linestyle = 'dotted' ,label = 'Utilidad generadores')
    axs[0].plot(conjunto_submultiplicadores, utilidades_tot_maxima, color = 'black', label = 'Utilidad maximizando ')

    axs[0].legend(loc='best',prop={'size': 6})
    axs[1].plot(conjunto_submultiplicadores, contaminacion,color = 'green', alpha = 0.8,linestyle = 'dashed' ,label = 'Contaminacion')
    axs[1].legend(loc='best',prop={'size': 6})
    axs[1].set_ylim(-1,101)
    axs[1].set_title("Contaminacion por submultiplicador")
    axs[1].set_xlabel("Submultiplicador")
    axs[1].set_ylabel("Nivel de contaminacion")
    plt.show()

def graficar_maximos_con_simulacion_dada(libros,lista_agentes):
    contaminacion = []
    utilidades_tot_maxima = []
    utilidades_generadores_max = []
    utilidades_afectados_max= []
    contaminacion_simulacion = []
    utilidades_tot_maxima_simulacion = []

    for libro in libros:
        lista_agentes = libro[1]
        cantidad_maxima = calcular_max(lista_agentes)
        contaminacion.append(cantidad_maxima[0])
        utilidades_tot_maxima.append(cantidad_maxima[1])
        utilidades_generadores_max.append(cantidad_maxima[3])
        utilidades_afectados_max.append(cantidad_maxima[2])
        contaminacion_simulacion.append(contaminacion_ofertas_aceptadas(libro[0])[-1])
        utilidades_tot_maxima_simulacion.append(utilidad_ofertas_aceptadas(libro[0],lista_agentes)[-1])



    fig, axs = plt.subplots(1,2)
    fig.set_figheight(6)
    fig.set_figwidth(10)


    axs[0].set_title("Utilidad maxima por submultiplicador")
    axs[0].set_xlabel("submultiplicador")
    axs[0].set_ylabel("utilidad")

    #axs[0].plot(conjunto_submultiplicadores,utilidades_afectados_max, color = 'red', alpha = 0.5,linestyle = 'dotted', label = 'abs(Utilidad afectados)')
    #axs[0].plot(conjunto_submultiplicadores, utilidades_generadores_max,color = 'blue', alpha = 0.5,linestyle = 'dotted' ,label = 'Utilidad generadores')

    axs[0].plot(conjunto_submultiplicadores, utilidades_tot_maxima_simulacion,color = 'black', alpha = 0.9,label = 'Utilidad maxima simulacion')
    axs[0].plot(conjunto_submultiplicadores, utilidades_tot_maxima, color = 'black', alpha = 0.3,linestyle = 'dotted',label = 'Utilidad maxima teorica')

    axs[0].legend(loc='best',prop={'size': 6})
    axs[1].plot(conjunto_submultiplicadores, contaminacion,color = 'green', alpha = 0.3,linestyle = 'dashed' ,label = 'Contaminacion teorica')
    axs[1].plot(conjunto_submultiplicadores, contaminacion_simulacion, color = 'green', alpha = 0.9 ,label = 'Contaminacion simulacion')
    axs[1].legend(loc='best',prop={'size': 6})
    axs[1].set_ylim(-10,110)
    axs[1].set_title("Contaminacion por submultiplicador")
    axs[1].set_xlabel("Submultiplicador")
    axs[1].set_ylabel("Nivel de contaminacion")
    plt.show()

########## encapsulamiento ###############

#Grafico cant de derechos por grupo con distintos costos de transaccion a lo largo de 6 simulaciones
def graficar1():
    derechos_adquiridos_afectados_gj = []
    derechos_adquiridos_generadores_gj =[]
    contaminaciones_gj = []
    for j in [0,100,300,1000]: 
        derechos_adquiridos_afectados_g = []
        derechos_adquiridos_generadores_g =[]
        contaminaciones_g = []
        for i in range(5):    
            cantidad_agentes = 110
            proporcion_afectados = 0.6
            densidad_grafo = 0.5
            costo_transaccion = j
            submultiplicador_afectados = 5000
            multiplicador_de_coordinacion = 0.0004
            multiplicador_de_utilidad = 10000
            contaminacion_maxima = 100   
            modo_informacion=True
            cantidad_de_ticks= 200
    
    
            mi_simulacion = sim.Simulacion()    
    
            mi_simulacion.simular(cantidad_agentes, proporcion_afectados, densidad_grafo, costo_transaccion, submultiplicador_afectados, multiplicador_de_coordinacion, multiplicador_de_utilidad, contaminacion_maxima, modo_informacion, cantidad_de_ticks)
            libro1=mi_simulacion.sacar_libro()
            mi_simulacion.finalizar_simulacion()
    
    
            mi_simulacion.simular(cantidad_agentes, proporcion_afectados, densidad_grafo, costo_transaccion, submultiplicador_afectados, multiplicador_de_coordinacion, multiplicador_de_utilidad, contaminacion_maxima, modo_informacion, cantidad_de_ticks)
            libro2=mi_simulacion.sacar_libro()
            mi_simulacion.finalizar_simulacion()
    
    
            a=libro1.info_por_tick
    
            contaminacion = [row[3] for row in a]
    
            derechos_adquiridos_generadores_g.append(derechos_adquiridos_generadores(a))
            derechos_adquiridos_afectados_g.append(derechos_adquiridos_afectados(a))
            contaminaciones_g.append(contaminacion)
            
        derechos_adquiridos_afectados_gj.append(derechos_adquiridos_afectados_g)
        derechos_adquiridos_generadores_gj.append(derechos_adquiridos_generadores_g)
        contaminaciones_gj.append(contaminaciones_g)
    
    graficar_derechos_para_distintos_costos_de_transaccion(derechos_adquiridos_generadores_gj,derechos_adquiridos_afectados_gj)

def graficar2(multiplicador_de_coordinacion, nombre):
    #seteamos para el grafo    
    cantidad_agentes = 61
    proporcion_afectados = 0.6
    densidad_grafo = 0.5
    costo_transaccion = 1000
    submultiplicador_afectados = 5000
    multiplicador_de_utilidad = 10000
    contaminacion_maxima = 100   
    modo_informacion=True
    cantidad_de_ticks= 100
    
    
    mi_simulacion = sim.Simulacion()    
    
    mi_simulacion.simular(cantidad_agentes, proporcion_afectados, densidad_grafo, costo_transaccion, submultiplicador_afectados, multiplicador_de_coordinacion, multiplicador_de_utilidad, contaminacion_maxima, modo_informacion, cantidad_de_ticks)
    libro1=mi_simulacion.sacar_libro()
    lista_agentes = mi_simulacion.lista_de_agentes
    mi_simulacion.finalizar_simulacion()
    
    
    a=libro1.info_por_tick
    grafica_grafo(nombre, multiplicador_de_coordinacion, a, lista_agentes)


################################################################################   
def graficar3(cantidad_agentes, proporcion_afectados, densidad_grafo, costo_transaccion, submultiplicador_afectados, multiplicador_de_coordinacion, multiplicador_de_utilidad, cantidad_de_ticks):
  modo_informacion=True  
  mi_simulacion = sim.Simulacion()    

  mi_simulacion.simular(cantidad_agentes, proporcion_afectados, densidad_grafo, costo_transaccion, submultiplicador_afectados, multiplicador_de_coordinacion, multiplicador_de_utilidad, 100, modo_informacion, cantidad_de_ticks)
  mi_simulacion.finalizar_simulacion()


  seq_contaminacion = sim.seq_contaminacion
  seq_cantidad_grupos = sim.seq_cantidad_grupos
  seq_cantidad_ofertas = sim.seq_cantidad_ofertas

  # Setting up the plot
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
  
  
##########################
def graficar4():
    conjunto_costos_transaccion = np.arange(0,200,10)
    
    lista_utilidades_totales=[0]*len(conjunto_costos_transaccion)
    lista_utilidades_totales_generadores=[0]*len(conjunto_costos_transaccion)
    lista_utilidades_totales_afectados=[0]*len(conjunto_costos_transaccion)
    
    contaminacion_teorica = [0]*len(conjunto_costos_transaccion)
    contaminacion_simulada = [0]*len(conjunto_costos_transaccion)
    
    lista_utilidades=[0]*len(conjunto_costos_transaccion)
    lista_utilidades_generadores=[0]*len(conjunto_costos_transaccion)
    lista_utilidades_afectados=[0]*len(conjunto_costos_transaccion)
    for i in range(len(conjunto_costos_transaccion)):
        for j in range(3):
            cantidad_agentes = 100
            proporcion_afectados = 0.7
            densidad_grafo = 0.5
            costo_transaccion = conjunto_costos_transaccion[i]
            submultiplicador_afectados = 550
            multiplicador_de_coordinacion = 0.0004 #0.0004
            multiplicador_de_utilidad = 1000
            contaminacion_maxima = 100   
            modo_informacion=True
            cantidad_de_ticks= 100
            
            mi_simulacion = sim.Simulacion()    
    
            mi_simulacion.simular(cantidad_agentes, proporcion_afectados, densidad_grafo, costo_transaccion, submultiplicador_afectados, multiplicador_de_coordinacion, multiplicador_de_utilidad, contaminacion_maxima, modo_informacion, cantidad_de_ticks)
        
            libro=mi_simulacion.sacar_libro()
            lista_agentes = mi_simulacion.lista_de_agentes
            
            tupla_optimos = calcular_max(lista_agentes)
            niv_contaminacion = tupla_optimos[0]
            utilidad_max = tupla_optimos[1]
            utilidad_afectados = tupla_optimos[2]
            utilidad_generadores = tupla_optimos[3]

            
            
            
            #return (optimo_contaminacion, optimo_util_total, optimo_util_afectados, optimo_util_generadores)
            #niv_contaminacion, utilidad_max, utilidad_generadores, utilidad_afectados = calcular_max(lista_agentes)

            
            lista_utilidades_totales[i]+=utilidad_max*1/3
            lista_utilidades_totales_generadores[i]+=utilidad_generadores*1/3
            lista_utilidades_totales_afectados[i]+=utilidad_afectados*1/3
            
            contaminacion_teorica[i] += niv_contaminacion * 1/3

            
            ultimas_ofertas_aceptadas=libro.info_por_tick[len(libro.info_por_tick)-1][1]
            utilidad_generadores2 = 0
            utilidad_afectados2 = 0
            contaminacion = 0
            for oferta in ultimas_ofertas_aceptadas:
                agente = lista_agentes[oferta[2]]
                if agente.tipo == 'generador':
                    utilidad_generadores2+=agente.tabla_de_utilidad[oferta[0]]
                    contaminacion += oferta[0]
            
            for agente in lista_agentes:
                if agente.tipo == 'afectado':
                    utilidad_afectados2 += agente.tabla_de_utilidad[contaminacion]
            
            ut_total=utilidad_generadores2+utilidad_afectados2
            lista_utilidades[i]+=ut_total*1/3
            lista_utilidades_generadores[i]+=utilidad_generadores2*1/3
            lista_utilidades_afectados[i]+=utilidad_afectados2*1/3 
            contaminacion_simulada[i] += contaminacion*1/3
            
            mi_simulacion.finalizar_simulacion()
            
    
            
    plt.title("Utilidades Totales Teoricas y Simuladas")
    plt.xlabel("Costo de Transacción")
    plt.ylabel("Utilidad")
    
    #plt.plot(conjunto_costos_transaccion, contaminacion_teorica, color = 'limegreen', alpha = 0.9, linestyle = 'dotted',label = 'Contaminacion Promedio Teorica')
    #plt.plot(conjunto_costos_transaccion, contaminacion_simulada, color = 'darkgreen', alpha = 0.9, label = 'Contaminacion Promedio Simulada')
    plt.plot(conjunto_costos_transaccion, lista_utilidades,color = 'blue', alpha = 0.9,label = 'Utilidad Total Simulada')
    plt.plot(conjunto_costos_transaccion, lista_utilidades_totales, color = 'red', alpha = 0.7,linestyle = 'dotted',label = 'Utilidad Total Teorica')
    
    plt.legend(loc='best',prop={'size': 6})
    plt.show()        
            
    plt.title("Utilidades de los Afectados Teoricas y Simuladas")
    plt.xlabel("Costo de Transacción")
    plt.ylabel("Utilidad")
    
    plt.plot(conjunto_costos_transaccion, lista_utilidades_afectados,color = 'blue', alpha = 0.9,label = 'Utilidad de los Afectados Simulada')
    plt.plot(conjunto_costos_transaccion, lista_utilidades_totales_afectados, color = 'red', alpha = 0.7,linestyle = 'dotted',label = 'Utilidad de los Afectados Teorica')
    
    plt.legend(loc='best',prop={'size': 6})
    plt.show()        
    
    plt.title("Utilidades de los Generadores Teoricas y Simuladas")
    plt.xlabel("Costo de Transacción")
    plt.ylabel("Utilidad")
    
    plt.plot(conjunto_costos_transaccion, lista_utilidades_generadores,color = 'blue', alpha = 0.9,label = 'Utilidad de los Generadores Simulada')
    plt.plot(conjunto_costos_transaccion, lista_utilidades_totales_generadores, color = 'red', alpha = 0.7,linestyle = 'dotted',label = 'Utilidad de los Generadores Teorica')
    
    plt.legend(loc='best',prop={'size': 6})
    plt.show()              
        
        
        