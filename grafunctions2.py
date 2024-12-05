import numpy as np
import matplotlib.pyplot as plt
import Simulacion2 as sim

import matplotlib.pyplot as plt

def fraccion_en_x(numero,p):
    fraccion= np.random.normal(numero, p)
    if fraccion < 0:
        return (np.abs(fraccion)%1)
    if fraccion > 1:
        return ((2-fraccion)%1)
    if(fraccion>1 or fraccion<0):
        raise ValueError('Error: Fraccion de x no normal')
    return fraccion    

def grafico1(media, varianza, sample_size, titulo):
    sample1_size=sample_size
    param1=media
    param2=varianza
    numbers1=np.zeros((sample1_size))
    for i in range(sample1_size):
        numbers1[i]=fraccion_en_x(param1, param2)
    
    plt.title(titulo)
    plt.hist(numbers1)
    plt.show()
    



 




def crear_agentes(cantidad_agentes, proporcion_afectados, submultiplicador_afectados, multiplicador_de_utilidad, contaminacion_maxima):
    mi_simulacion = sim.Simulacion()
    
    cantidad_afectados = int(round(cantidad_agentes * proporcion_afectados))
    cantidad_generadores = cantidad_agentes - cantidad_afectados
    submultiplicador_generadores = multiplicador_de_utilidad - submultiplicador_afectados
    submultiplicador_afectado_individual = (submultiplicador_afectados / cantidad_afectados)
    submultiplicador_generador_individual = (submultiplicador_generadores / cantidad_generadores)
    
    lista_de_agentes = mi_simulacion.generar_lista_de_agentes(submultiplicador_afectado_individual, submultiplicador_generador_individual, cantidad_afectados, cantidad_generadores, mi_simulacion)
    mi_simulacion.finalizar_simulacion()
    return lista_de_agentes

def sum_nth_elements(list_of_lists):
    # Initialize the result list with 101 zeros
    result = [0] * 101
    
    # Loop through each inner list
    for inner_list in list_of_lists:
        # Loop through each element in the inner list
        for i in range(101):
            result[i] += inner_list[i]
    
    return result

def grafico2(agentes):
    tablas_de_utilidad_de_afectados = []
    tablas_de_utilidad_de_generadores = []
    tabla_de_utilidad_de_afectados_conjunta = []

    for agente in agentes:
        if agente.tipo == "afectado":
            tablas_de_utilidad_de_afectados.append(agente.tabla_de_utilidad)
        if agente.tipo == "generador":
            tablas_de_utilidad_de_generadores.append(agente.tabla_de_utilidad)



    tabla_de_utilidad_de_afectados_conjunta = sum_nth_elements(tablas_de_utilidad_de_afectados)

    # Plot all the inner tables of tablas_de_utilidad_de_afectados on the same plot
    plt.figure(figsize=(10, 6))
    for tabla in tablas_de_utilidad_de_afectados:
        plt.plot(tabla)
    plt.title('Funciones de Utilidad de Afectados')
    plt.xlabel('Nivel de Contaminacion')
    plt.ylabel('Utilidad')
    plt.show()
    
    # Plot all the inner tables of tablas_de_utilidad_de_afectados on the same plot
    plt.figure(figsize=(10, 6))
    for tabla in tablas_de_utilidad_de_generadores:
        plt.plot(tabla)
    plt.title('Funciones de Utilidad de Generadores')
    plt.xlabel('Derechos del Generador')
    plt.ylabel('Utilidad')
    plt.show()
    
    # Plot tabla_de_utilidad_de_afectados_conjunta on one plot
    plt.figure(figsize=(10, 6))
    plt.plot(tabla_de_utilidad_de_afectados_conjunta, label='Conjunta Utility')
    plt.title('Tabla de Utilidad de Afectados Conjunta')
    plt.xlabel('Nivel de Contaminacion')
    plt.ylabel('Utilidad conjunta')
    plt.show()



