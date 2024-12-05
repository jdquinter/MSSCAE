
import numpy as np
import random
        
    
class Agente:
        def __init__(self, identificador, tipo):
               self.id = identificador
               self.tipo = tipo
               self.funcion_utilidad = None
               self.tabla_de_utilidad = None
        
               self.sim = None

