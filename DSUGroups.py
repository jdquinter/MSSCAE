


""" 
.ofertar_con_su_grupo(nodo):
Caso Afectados:
Devuelve (movimiento en x signado, utilidad ofrecida, id_del_grupo, fraccion_ofrecida)

"""
import numpy as np
        

class DSUGroups:
    
    def __init__(self, list_nodes, sim=None):
        
        self.__lista_padres = list_nodes
        
        self.__lista_integrantes_del_grupo=[]
        for i in range(len(list_nodes)):
            self.__lista_integrantes_del_grupo.append([i])
        
        self.__el_grupo_oferto_este_tick=[]
        for i in range(len(list_nodes)):
            self.__el_grupo_oferto_este_tick.append(False)
            
        self.__lista_pisos_de_fracciones=[]
        for i in range(len(list_nodes)):
            self.__lista_pisos_de_fracciones.append(0.15)
            
        self.__lista_ofertas=[]
        for i in range(len(list_nodes)):
            self.__lista_ofertas.append((None, False))
            
            
        
        self.nivel_contaminacion_anterior=0
        
        if (sim is None): 
            self.__sim= None
            self.__dist_minima_a_propietario_del_grupo=[]
            
        else:
            self.__sim = sim
            self.__dist_minima_a_propietario_del_grupo=self.__sim.grafo.lista_caminos_minimos(0) 
            
    
            
    
    def padre_por_nodo(self):
        return self.__lista_padres
                
                            
            
    def set_sim(self, sim):
        
        if(self.__sim is not None):
            raise ValueError("Ya estas conectado a una simulacion")
        self.__sim=sim
        

        self.__dist_minima_a_propietario_del_grupo=self.__sim.grafo.lista_caminos_minimos(0)

                    
            
            
    def find_group(self, node):
        
        if(self.__sim is None):
            raise ValueError("No conectado a la simulacion")
        if self.__lista_padres[node] == node:
            return node
        else:
            res = self.find_group(self.__lista_padres[node])
            self.__lista_padres[node] = res
            return res    



    def union(self, node1, node2):
        
        if(self.__sim is None):
            raise ValueError("No conectado a la simulacion")
        
        # A la lista de integrates del grupo del nodo 2 le añade la lista del nodo 1
        for member in self.__lista_integrantes_del_grupo[self.find_group(node1)]:
            self.__lista_integrantes_del_grupo[self.find_group(node2)].append(member)
        
        # Actualiza la distancia minima
        if(self.dist_min_al_propietario(node1) > self.dist_min_al_propietario(node2)):
            self.__dist_minima_a_propietario_del_grupo[self.find_group(node2)] =  self.dist_min_al_propietario(node1)
        
        # Hace promedio de las medias de los grupos
        mu1=self.__lista_pisos_de_fracciones[self.find_group(node1)]
        mu2=self.__lista_pisos_de_fracciones[self.find_group(node2)]
        size1=len(self.__lista_integrantes_del_grupo[self.find_group(node1)])
        size2=len(self.__lista_integrantes_del_grupo[self.find_group(node2)])
        new_mu=(mu1*size1+mu2*size2)/(size1+size2)
        self.__lista_pisos_de_fracciones[self.find_group(node2)]=new_mu ##AGREGA UN FLOAT Y DESPUES QUIERE IDENTAR CON ESTO.
        
        if(self.__lista_ofertas[self.find_group(node1)][1]==True and self.__lista_ofertas[self.find_group(node2)][1]==True):
            oferta1=self.__lista_ofertas[self.find_group(node1)][0]
            oferta2=self.__lista_ofertas[self.find_group(node2)][0]
            if(oferta1[0]*oferta2[1]>oferta2[0]*oferta1[1]):
                self.__lista_ofertas[self.find_group(node2)]=self.__lista_ofertas[self.find_group(node1)]
        elif(self.__lista_ofertas[self.find_group(node1)][1]==True):    
             self.__lista_ofertas[self.find_group(node2)]=self.__lista_ofertas[self.find_group(node1)]
            

        
        
        #Setea el padre del nodo 1 aser igual al padre del nodo 2
        self.__lista_padres[self.find_group(node1)] = self.find_group(node2)
        

               
    def dist_min_al_propietario(self, node):
        return self.__dist_minima_a_propietario_del_grupo[self.find_group(node)]
        
        
        
    def are_same_group(self, nodo1, nodo2):
        
        if(self.__sim is None):
            raise ValueError("No conectado a la simulacion")
        return self.find_group(nodo1)==self.find_group(nodo2)
    
    
    
    def integrantes(self, nodo):
        
        if(self.__sim is None):
            raise ValueError("No conectado a la simulacion")
        
        return self.__lista_integrantes_del_grupo[self.find_group(nodo)]
    
    
    
    def realizo_oferta_este_tick(self, nodo):
        
        if(self.__sim is None):
            raise ValueError("No conectado a la simulacion")
        
        return self.__el_grupo_oferto_este_tick[self.find_group(nodo)]
    
    
    
    def nuevo_tick(self):
        
        if(self.__sim is None):
            raise ValueError("No conectado a la simulacion")
        
        for i in range(len(self.__el_grupo_oferto_este_tick)):
            self.__el_grupo_oferto_este_tick[i]= False
            
            
                   
    
    def lista_grupos(self):
        lista_grupos=[]
        for node in range(len(self.__lista_padres)):
            if (node == self.find_group(node)) and node != 0:
                lista_grupos.append(node)               
        return lista_grupos    
 
 

    def fraccion_en_x(self, media, varianza):
        fraccion= np.random.normal(media, varianza)
        if fraccion < 0:
            return (np.abs(fraccion)%1)
        if fraccion > 1:
            return ((2-fraccion)%1)
        if(fraccion>1 or fraccion<0):
            raise ValueError('Error: Fraccion de x no normal')
        return fraccion   


    def fracaso_oferta(self, nodo):
        if(self.__lista_pisos_de_fracciones[self.find_group(nodo)] + 0.1 >=1):
            self.__lista_pisos_de_fracciones[self.find_group(nodo)] = 1 
        else:
            self.__lista_pisos_de_fracciones[self.find_group(nodo)] += 0.1



    def ofertas_aceptadas(self, ofertas_aceptadas, niv):
        
        self.nivel_contaminacion_anterior=niv
        
        for oferta in ofertas_aceptadas:
            ofertante = oferta[2]
            representante = self.find_group(ofertante)
            self.__lista_ofertas[representante] = (oferta, True)
            
        for i in self.lista_grupos():
            if(self.__lista_ofertas[i][1]==False):
                self.fracaso_oferta(i)



    def ofertar_con_su_grupo(self, node):
            
        
        
            if(self.__sim is None):
                raise ValueError("No conectado a la simulacion")
            
            if(self.realizo_oferta_este_tick(node)):
                raise ValueError(f"Ya realizo una oferta el grupo del agente {node}")
        

            self.__el_grupo_oferto_este_tick[self.find_group(node)]=True
            
                
            ### El nodo es un generador
            if(self.sim.lista_de_agentes[node].tipo == "generador"):
                               
                agente=self.sim.lista_de_agentes[node]
                
                #####
                media_x=0
                varianza_x=0.25
                varianza_u=0.05
                """
                if self.__lista_ofertas[self.find_group(node)][1]==True:
                    media_x=0.55
                """
                ####
                
                a=self.fraccion_en_x(media_x, varianza_x)  
                movimiento_en_contaminacion=int((self.__sim.nivel_de_contaminacion_maximo)*a)
                utilidad_en_tabla = agente.tabla_de_utilidad[movimiento_en_contaminacion]
                
                if(movimiento_en_contaminacion==0 and utilidad_en_tabla>0):
                    raise ValueError('Error: Oferta desplazamiento 0 utilidad positiva')  
                     
                fraccion_de_utilidad = self.fraccion_en_x(self.__lista_pisos_de_fracciones[self.find_group(node)], varianza_u)
                utilidad_ofrecida = utilidad_en_tabla*fraccion_de_utilidad - self.dist_min_al_propietario(node)
                oferta_nueva=(movimiento_en_contaminacion, utilidad_ofrecida, self.find_group(node), fraccion_de_utilidad)

            
                if self.__lista_ofertas[self.find_group(node)][1]==False:
                    #No le aceptaron ofertas anteriores
                    if oferta_nueva[1] > 0:
                        return [oferta_nueva]
                    else:
                        self.fracaso_oferta(node)
                        return []
                    
                else:
                    oferta_vieja=self.__lista_ofertas[self.find_group(node)][0]
                    
                    if(oferta_nueva[0]<=oferta_vieja[0] or oferta_nueva[1]<0):
                        return [oferta_vieja]
                    else:
                        return [oferta_vieja, oferta_nueva]
                        
                                       
            ### El nodo es un afectado
            if(self.sim.lista_de_agentes[node].tipo == "afectado"):
                
                
                #####
                media_x=0.25
                varianza_x=0.39
                varianza_u=0.05      
                """
                if self.__lista_ofertas[self.find_group(node)][1]==True:
                    media_x=0.45
                    """
                ####
                
                a=self.fraccion_en_x(media_x, varianza_x)
                movimiento_en_contaminacion=int((self.__sim.nivel_de_contaminacion)*a  )                          
                
                suma_de_utilidades_tabla = 0
                for identficador in self.integrantes(node):   
                    agente_integrante = self.sim.lista_de_agentes[identficador]
                    valor=np.abs(agente_integrante.tabla_de_utilidad[self.__sim.nivel_de_contaminacion] - agente_integrante.tabla_de_utilidad[self.__sim.nivel_de_contaminacion-movimiento_en_contaminacion])                
                    
                    if(movimiento_en_contaminacion==0 and valor>0):
                        raise ValueError('Error: Un generador ofrece utilidad por desplazamiento 0') 
                    
                    suma_de_utilidades_tabla +=valor
                    
                if(movimiento_en_contaminacion==0 and suma_de_utilidades_tabla>0):
                    raise ValueError('Error: Oferta desplazamiento 0 suma de utilidad positiva') 
                
                
                fraccion_de_utilidad_grupo = self.fraccion_en_x(self.__lista_pisos_de_fracciones[self.find_group(node)], varianza_u)
                utilidad_ofrecida = suma_de_utilidades_tabla*fraccion_de_utilidad_grupo - self.dist_min_al_propietario(node)
                oferta_nueva=(-movimiento_en_contaminacion, utilidad_ofrecida, self.find_group(node), fraccion_de_utilidad_grupo)
                
                if(abs( oferta_nueva[0])>self.__sim.nivel_de_contaminacion):
                    raise ValueError('Error: estamos haciendo oferta imposible') 
                    
                if self.__lista_ofertas[self.find_group(node)][1]==False:
                    #No le aceptaron ofertas anteriores
                    if oferta_nueva[1] > 0:
                        return [oferta_nueva]
                    else:
                        self.fracaso_oferta(self.find_group(node))
                        return []
                    
                else:
                    oferta_en_lista = self.__lista_ofertas[self.find_group(node)][0]
                    #print(self.__lista_ofertas[self.find_group(node)], 'nivel_cont_anterior', self.nivel_contaminacion_anterior)
                    #print('cantaminacion:', self.__sim.nivel_de_contaminacion)
                    nivel_contaminacion_anterior=self.nivel_contaminacion_anterior
                    

                    
                    suma_de_utilidades_oferta_vieja = 0
                    for identficador in self.integrantes(node):   
                        agente_integrante = self.sim.lista_de_agentes[identficador]
                        valor=np.abs(agente_integrante.tabla_de_utilidad[nivel_contaminacion_anterior] - agente_integrante.tabla_de_utilidad[nivel_contaminacion_anterior+oferta_en_lista[0]])                
                        
                        if(oferta_en_lista[0]==0 and valor>0):
                            raise ValueError('Error: Un generador ofrece utilidad por desplazamiento en oferta vieja 0') 
                        
                        suma_de_utilidades_oferta_vieja +=valor
                    
                    
                    oferta_vieja=(oferta_en_lista[0],
                                  oferta_en_lista[1],
                                  self.find_group(node),
                                  oferta_en_lista[1]/(suma_de_utilidades_oferta_vieja-self.dist_min_al_propietario(node))
                                  )
                    
                    if(np.abs(oferta_nueva[0]) <= np.abs(oferta_vieja[0]) or oferta_nueva[1]<0):
                        return [oferta_vieja]
                    else:
                        return [oferta_vieja, oferta_nueva]
                        

                        
                        
                        
#(movimiento en x signado, utilidad ofrecida, id_del_grupo, fraccion_ofrecida)