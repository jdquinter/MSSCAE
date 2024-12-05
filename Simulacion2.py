import sys

sys.path.append('C:/Users/santi/Desktop/tp_msscae')

import random
import numpy as np
import copy 
import Agente as ag
import Grafo as grafo
import DSUGroups as dsu

seq_contaminacion = []
seq_cantidad_grupos = []
seq_cantidad_ofertas = []

class Simulacion:
    def __init__(self):
        # pregunta: utilidad_total_actual y utilidad_total_acumulada como parametros globales para hacer mas facil los graficos?
        # comentario: siempre va a haber 100 unidades de contaminacion como maximo y 100 unidades de derechos en total.
        # comentario: el propietario considera las ofertas eligiendo el mejor bundle posible entre los derechos asignados previamente y las ofertas nuevas
        # (es decir, el que maximiza el dinero recibido).
        # !!! hacer 'tipo'/clase para ID, derechos, nivel de contaminacion, etc, con sus respectivos rangos aceptables.
        # !!! despues vamos a necesitar mas parametros para guardar la informacion que vamos a usar para graficar.

        # Una lista de los hiperparametros de la simulacion y sus valores,
        # representados como tuplas (nombre: str, valor).
        # Los hiperparametros van a ser:
        #   - Cantidad de agentes
        #   - Proporcion de afectados (#afectados/#agentes)
        #   - Densidad del grafo: float entre [0,1] (define la densidad de de conexiones en el grafo)
        #   - Costo de transaccion: (define la distribucion de los pesos de las aristas del grafo)
        #       (se multiplica por un numero aleatorio entre [0,1])
        #   - Contaminacion maxima & derechos = 100
        #   - Multiplicador de utilidad = 1000
        #   - Submultiplicador de los afectados: int entre [0, Multiplicador de utilidad].
        #       (el de los generadores es el complemento = 1000 - Submultiplicador de los afectados)
        self.hiperparametros = []
        
        # Es un entero que representa el tiempo transcurrido en la simulacion.
        # Cada unidad representa una ronda transcurrida.
        self.tick = 0
        
        self.nivel_de_contaminacion_maximo = 0
        
        # Es el nivel de contaminacion global, que se mueve entre 0 y 100
        self.nivel_de_contaminacion = 0

        self.multiplicador_de_coordinacion = 0
        
        
        # Es una lista de objetos de la clase Agente, que pueden ser agentes afectados o generadores.
        # Su indice en la lista es su ID unico identificador.
        # El tipo de un agente lo define un string tipo_del_agente = "afectado" || "generador" || "propietario" .
        self.lista_de_agentes = []
        
        self.cantidad_generadores = 0

        # Es una lista de ofertas, que tendra las ofertas hechas en la ronda que luego considerara el propietario.
        # Se reseteara a [] despues de cada ronda.
        self.lista_de_ofertas = []
        self.ofertas_aceptadas = []

        # El grafo pesado no-dirigido que contiene a todos los agentes
        self.grafo = grafo.Grafo()

        self.grupos = dsu.DSUGroups([])
        
        self.modo_informacion = False
        
        self.book_of_information = None
        


    def simular(self, cantidad_agentes, proporcion_afectados, densidad_grafo, costo_transaccion, submultiplicador_afectados, multiplicador_de_coordinacion, multiplicador_de_utilidad, contaminacion_maxima, modo_informacion, cantidad_de_ticks):

        #print('Iniciando simulacion...')
        self.inicializar_simulacion(cantidad_agentes, proporcion_afectados, densidad_grafo, costo_transaccion, submultiplicador_afectados, multiplicador_de_coordinacion, multiplicador_de_utilidad, contaminacion_maxima, modo_informacion, cantidad_de_ticks)
        
        while (self.tick < self.cantidad_de_ticks ):  
            #print(f' Tick: {self.tick}')
            
            self.los_grupos_ofertan()
            #print(f'Los grupos ofertaron: {len(self.lista_de_ofertas)} ofertas')
            
            seq_cantidad_ofertas.append(len(self.lista_de_ofertas))
            
            if(len(self.lista_de_ofertas)>2*len(self.lista_de_agentes)):
                raise ValueError('Error: Demasiadas ofertas')
                
                
            self.propiertario_acepta_ofertas()
            #print('El propietario eligio las ofertas')
            
            
            self.terminar_tick()
            #print('Se actualizo el modelo')
      
            
      
    def finalizar_simulacion(self):
        self.tick = 0        
        self.nivel_de_contaminacion_maximo = 0      
        self.nivel_de_contaminacion = 0
        self.multiplicador_de_coordinacion = 0
        self.lista_de_agentes = []
        self.lista_de_ofertas = []
        self.ofertas_aceptadas = []
        self.grafo = grafo.Grafo()
        self.grupos = dsu.DSUGroups([])        
        self.modo_informacion = False       
        self.book_of_information = None    
        
        
            
    def inicializar_simulacion(
                    self,
                    cantidad_agentes,
                    proporcion_afectados,
                    densidad_grafo,
                    costo_transaccion,
                    submultiplicador_afectados,
                    multiplicador_de_coordinacion,
                    multiplicador_de_utilidad,
                    contaminacion_maxima,
                    modo_informacion, 
                    cant_ticks_max):
    
        cantidad_afectados = int(round(cantidad_agentes * proporcion_afectados))
        cantidad_generadores = cantidad_agentes - cantidad_afectados
        submultiplicador_generadores = multiplicador_de_utilidad - submultiplicador_afectados


        self.hiperparametros = [("cantidad_agentes", cantidad_agentes), ("proporcion_afectados", proporcion_afectados),
                            ("densidad_grafo", densidad_grafo), ("costo_transaccion", costo_transaccion),
                            ("submultiplicador_afectados", submultiplicador_afectados), ("multiplicador_de_coordinacion", multiplicador_de_coordinacion),
                            ("multiplicador_de_utilidad", multiplicador_de_utilidad), ("contaminacion_maxima", contaminacion_maxima)]
        
        self.multiplicador_de_coordinacion = multiplicador_de_coordinacion
        self.nivel_de_contaminacion_maximo = contaminacion_maxima

        self.cantidad_generadores = cantidad_generadores
        submultiplicador_afectado_individual = (submultiplicador_afectados / cantidad_afectados)
        submultiplicador_generador_individual = (submultiplicador_generadores / 4) #(submultiplicador_generadores / cantidad_generadores)
        
        lista_de_agentes = self.generar_lista_de_agentes(submultiplicador_afectado_individual, submultiplicador_generador_individual, cantidad_afectados, cantidad_generadores,self)
        self.lista_de_agentes = lista_de_agentes
        
        

        tabla_de_pagos = []
        for i in range(cantidad_agentes):
            tabla_de_pagos.append([])
        self.tabla_de_pagos = tabla_de_pagos

        self.grafo = grafo.Grafo()
        self.grafo.generador_grafo(densidad_grafo, costo_transaccion, cantidad_agentes)

        lista_de_ids = [i for i in range(cantidad_agentes)]
        self.grupos = dsu.DSUGroups(lista_de_ids,self)
        self.grupos.sim = self
        
        self.cantidad_de_ticks = cant_ticks_max
        
        if(modo_informacion == True):
            self.modo_informacion = modo_informacion
            pointer=self
            self.book_of_information = LibroInformativo(pointer, cant_ticks_max)
        return

    

    def generar_lista_de_agentes(self,submultiplicador_afectados, submultiplicador_generadores, cantidad_afectados, cantidad_generadores, simulacion):
    
        lista_de_agentes = []
        
        lista_de_agentes.append(ag.Agente(0, "propietario"))
        for i in range(1,cantidad_generadores):
            lista_de_agentes.append(self.generar_agente(i, submultiplicador_generadores, "generador", simulacion))
        for i in range(cantidad_afectados):
            lista_de_agentes.append(self.generar_agente(i + cantidad_generadores, submultiplicador_afectados, "afectado", simulacion))
        
        return lista_de_agentes   



    def generar_agente(self,id_del_agente, submultiplicador_del_agente, tipo_del_agente, simulacion):
        agente = ag.Agente(id_del_agente, tipo_del_agente)
        # (repito el codigo adentro de los ifs por si despues queremos diferenciar
        # esos aspectos de la generacion entre afectados y generadores)
        if tipo_del_agente == "afectado":
            k = submultiplicador_del_agente
            alpha_costo = random.uniform(0.001, 0.1)
            def costo(contaminacion):
                return -1 * (k - k * np.exp(-alpha_costo * contaminacion))
            agente.funcion_utilidad = costo
            tabla = np.arange(102)
            tabla = list(map(costo, tabla))
            agente.tabla_de_utilidad = tabla
            # agente.tabla_de_utilidad[i] me da la utilidad que le asigna el agente al
            # estado i (i unidades de contaminacion).
    
        elif tipo_del_agente == "generador":
            k = submultiplicador_del_agente
            alpha_beneficio = random.uniform(0.001, 0.1)
            def beneficio(derechos):
                return k - (k * np.exp(-alpha_beneficio * derechos))
            agente.funcion_utilidad = beneficio
            tabla = np.arange(101)
            tabla = list(map(beneficio, tabla))
            agente.tabla_de_utilidad = tabla
            # agente.tabla_de_utilidad[i] me da la utilidad que le asigna el agente al
            # estado i (i derechos).
            
        #else: tipo_del_agene == "propietario", no hay que hacer nada mas
    
        agente.sim = simulacion
    
        return agente



    #Metodo que agarra todas las ofertas de los grupos y las mete en la lista de ofertas. Correr despues de actualizar grupos
    def los_grupos_ofertan(self):         
        
        lista_de_grupos = self.grupos.lista_grupos()
        for node_id in lista_de_grupos:
            for oferta in self.grupos.ofertar_con_su_grupo(node_id):
                self.lista_de_ofertas.append(oferta)
                if(oferta[1]<0):
                    raise ValueError(f'Error: Oferta invalida {oferta}')
                if(oferta[0]==0 and oferta[1]>0):
                    raise ValueError(f'Error: Oferta desplazamiento 0 utilidad positiva {oferta}')

                    

    #Metodos para aceptar las ofertas dadas                    
    def propiertario_acepta_ofertas(self):
        
        ofertas = copy.deepcopy(self.lista_de_ofertas)
        ofertas=self.armar_ofertas_sin_grupos_repetidos(ofertas)
        self.ofertas_aceptadas=ofertas

        
        
    
    def armar_ofertas_sin_grupos_repetidos(self, ofertas):
        
        if (ofertas == [] or ofertas == None):
            return []
        
        repetido = True
        while repetido:
            repetido = False
            tupla = self.indices_ofertas_seleccionadas(ofertas)
            #print(ofertas)
            #print("TUPLA TUPLA") #debug
            #print(tupla) #debug
            conjunto_ofertas = tupla[0]
            grupo_en_el_conjunto = [False]*len(self.lista_de_agentes)
            for oferta in conjunto_ofertas:
                id_grupo = ofertas[oferta][2]
                if grupo_en_el_conjunto[id_grupo]==False:
                    grupo_en_el_conjunto[id_grupo]=True
                
                else:
                    repetido = True
                    #eliminar oferta
                    id_a_eliminar=0
                    for revisar in conjunto_ofertas:
                        ratio=0
                           
                        if(id_grupo==ofertas[revisar][2] and (np.abs(ofertas[revisar][0])==0 or np.abs(ofertas[revisar][0])/ofertas[revisar][1]<ratio)):                                
                            if(np.abs(ofertas[revisar][0])==0):
                                if(ofertas[revisar][1]==0):
                                    ratio=0
                                    raise ValueError(f'Error: Oferta ofrece 0 {ofertas[revisar]}')
                                else:
                                    ratio=float('inf')
                                    raise ValueError(f'Error: Oferta intervalo 0 {ofertas[revisar]}')
                            else:                                
                                ratio=np.abs(ofertas[revisar][0])/ofertas[revisar][1]
                                                   
                            id_a_eliminar=revisar
                                                        
                    ofertas.pop(id_a_eliminar)
                    break
        res=[]
        for oferta in conjunto_ofertas:
            res.append(ofertas[oferta])
        return res
    
    
    
    def indices_ofertas_seleccionadas(self, ofertas):
        
        #DEBUG DEBUG CAUSA UN ERROR, DEVUELVE A VECES NONE
        #if (ofertas == []):
         #   return ([],0)
        
        
        #cantidad maxima de plarta que puede recibir el prop por tick
            cantidad_maxima=self.nivel_de_contaminacion_maximo 
            cant_ofertas = len(ofertas)  
            
            dp = [[0] * (cantidad_maxima + 1) for _ in range(cant_ofertas)]
            selected = [[False] * (cantidad_maxima + 1) for _ in range(cant_ofertas)]
            
            for derechos_disponibles in range(cantidad_maxima + 1):
                if (ofertas == []): # DEBUG DEBUG
                    continue
                if(derechos_disponibles>= np.abs(ofertas[0][0])):
                    #ver si no tiene q ser un ofertas[0][0]
                    dp[0][derechos_disponibles]=np.abs(ofertas[0][0])
                    selected[0][derechos_disponibles]=True
            
            for nro_oferta in range(1, cant_ofertas):
                cantidad_derechos_oferta = np.abs(ofertas[nro_oferta][0])
                precio = ofertas[nro_oferta][1]
                for derechos_disponibles in range(cantidad_maxima + 1):
                    if derechos_disponibles >= cantidad_derechos_oferta:
                        if dp[nro_oferta-1][derechos_disponibles] >= dp[nro_oferta-1][derechos_disponibles - cantidad_derechos_oferta] + precio:
                            dp[nro_oferta][derechos_disponibles] = dp[nro_oferta-1][derechos_disponibles]
                            selected[nro_oferta][derechos_disponibles] = False
                        else:
                            dp[nro_oferta][derechos_disponibles] = dp[nro_oferta-1][derechos_disponibles - cantidad_derechos_oferta] + precio
                            selected[nro_oferta][derechos_disponibles] = True
                    else:
                        dp[nro_oferta][derechos_disponibles] = dp[nro_oferta-1][derechos_disponibles]
                        selected[nro_oferta][derechos_disponibles] = False
            
            
            conjunto_seleccionado = []
            a=cant_ofertas-1
            b=cantidad_maxima            
            while a>=0:
                if selected[a][b]==True:
                    conjunto_seleccionado.append(a)
                    b-= np.abs(ofertas[a][0])
                    a-=1

                else:
                    a-=1
     
            return (conjunto_seleccionado, dp[cant_ofertas-1][cantidad_maxima])    
      


    #Pasar a tick siguiente actualizando todo lo que es necesario
    def terminar_tick(self):
        if self.modo_informacion==True:
            self.book_of_information.actualizar(self.tick)
        
        nivel_anterior=self.nivel_de_contaminacion
        #print('nivel actual:', nivel_anterior)
        #print('cantidad de grupos: ', len(self.grupos.lista_grupos())-self.cantidad_generadores + 1)
        seq_contaminacion.append(nivel_anterior)
        seq_cantidad_grupos.append(len(self.grupos.lista_grupos())-self.cantidad_generadores + 1)
        self.actualizar_contaminacion()
        self.actualizar_grupos()
        self.grupos.nuevo_tick()
        self.tick += 1
        
        
        self.grupos.ofertas_aceptadas(self.ofertas_aceptadas, nivel_anterior)
        self.ofertas_aceptadas = []
        self.lista_de_ofertas=[]
                      
        
        
    #Para cada agente, ver su probabilidad de formar grupo (funcion de la derivada de la utilidad) y correr un random con cada uno de sus vecinos para ver si forman grupo
    def actualizar_grupos(self):
        for agente in self.lista_de_agentes:
            if agente.tipo == 'afectado': 
                utilidad_actual = agente.tabla_de_utilidad[self.nivel_de_contaminacion]
                utilidad_minima = agente.tabla_de_utilidad[self.nivel_de_contaminacion_maximo]
                probabilidad_de_formar_grupo = abs((utilidad_actual / utilidad_minima) * self.multiplicador_de_coordinacion)
                for arista in self.grafo.adyacencias[agente.id]:
                    if(self.lista_de_agentes[arista[0]].tipo == 'afectado'):
                        hace_grupo = random.random() < probabilidad_de_formar_grupo     
                        if hace_grupo and not self.grupos.are_same_group(agente.id,arista[0]):  
                            self.grupos.union(agente.id, arista[0])                              



    def actualizar_contaminacion(self):
            self.nivel_de_contaminacion = 0
            
            for oferta in self.ofertas_aceptadas:
                if(oferta[0]>0):
                   if(self.lista_de_agentes[oferta[2]].tipo == 'generador'):
                    self.nivel_de_contaminacion += oferta[0]
                   #self.nivel_de_contaminacion += oferta[0] 
            
            if self.nivel_de_contaminacion>self.nivel_de_contaminacion_maximo:
                raise ValueError('Error: Nivel de Contaminacion supera lo permitido al actualizarla')


    def sacar_libro(self):
        if(self.modo_informacion==False):
            raise ValueError('Modo informacion desactivado')
        self.book_of_information.simulacion=None
        return copy.deepcopy(self.book_of_information)
     
#########################################################################################################


        

class LibroInformativo:
    def __init__(self, sim, cantidad_ticks):
        self.simulacion=sim
        self.info_por_tick=[None]*cantidad_ticks
        self.info_inicial=(copy.deepcopy(sim.lista_de_agentes), copy.deepcopy(sim.grafo))

    def actualizar(self, tick):
        self.info_por_tick[tick]=(copy.deepcopy(self.simulacion.lista_de_ofertas), copy.deepcopy(self.simulacion.ofertas_aceptadas), copy.deepcopy(self.simulacion.grupos.padre_por_nodo()),copy.deepcopy(self.simulacion.nivel_de_contaminacion))
    