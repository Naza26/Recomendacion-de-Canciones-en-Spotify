import random

class Grafo:

    def __init__(self): 
        self.grafo = {} 
        self.grado_vertices = {}
        self.rol = {}

    def agregar_vertice(self, vertice, rol_vertice = None):
        '''Agrega un vertice al grafo. Su complejidad es O(1)'''
        self.grafo[vertice] = {}
        self.grado_vertices[vertice] = 0
        if rol_vertice not in self.rol: 
            self.rol[rol_vertice] = []
        self.rol[rol_vertice].append(vertice)

    def obtener_rol(self, vertice):
        for rol in self.rol: 
            if vertice in self.rol[rol]: 
                return rol

        
    def borrar_vertice(self, vertice):
        '''Borra un vertice del grafo. Su complejidad es O(1)'''
        if vertice not in self.grafo:
            return
        for w in self.obtener_vertices():
            if self.estan_unidos(vertice, w): 
                self.borrar_arista(vertice, w)
        self.grafo.pop(vertice)
        self.grado_vertices.pop(vertice)
    
    
    def agregar_arista(self, v, w, peso = 1): 
        '''Agrega una arista al grafo. Su complejidad es O(1)'''
        self.grafo[v][w] = peso 
        self.grafo[w][v] = peso 
        self.grado_vertices[v] += 1
        self.grado_vertices[w] += 1

    def borrar_arista(self, v, w):
        '''Borra una arista del grafo.'''
        self.grafo[v].pop(w)
        self.grafo[w].pop(v)
        self.grado_vertices[v] -= 1
        self.grado_vertices[w] -= 1

    def estan_unidos(self, v, w):
        '''Devuelve True si los vertices pasados por parametro estan unidos'''
        if not self.vertice_pertenece(v) or not self.vertice_pertenece(w):
            return False
        return (w in self.grafo[v])
    
    def peso_arista(self, v, w):
        '''Devuelve el peso de la arista'''
        return self.grafo[v][w]
    
    def obtener_grado_vertices(self):
        '''Devuelve un diccionario con los grados de los vertices del grafo'''
        return self.grado_vertices
    
    def obtener_vertices(self): 
        '''Devuelve una lista con los vertices del grafo'''
        return list(self.grafo.keys())

    def vertice_aleatorio(self):
        '''Devuelve un vertice aleatorio entre los vertices del grafo'''
        return random.choice(self.obtener_vertices())

    def adyacentes(self, v):
        '''Devuelve una lista con los adyacentes al vertice dado'''
        return list(self.grafo[v].keys())
    
    def vertice_pertenece(self, v):
        '''Devuelve True si el vertice pertenece al grafo'''
        return (v in self.grafo)
    
    def __str__(self):
        return f"{self.grafo}"

    def __len__(self):
        '''Devuelve la cantidad de vertices del grafo'''
        return len(self.grafo)
