from grafo import Grafo
import collections
import random

D = 0.85

def camino_minimo_bfs(grafo, inicio, fin):
    '''Esta función devuelve el camino mínimo entre un vértice origen y un vértice destino'''
    visitados = set()
    padres = {}
    camino_minimo = []
    distancias = {}
    padres[inicio] = None
    camino_minimo.append(inicio)
    distancias[inicio] = 0
    if inicio == fin: 
        return padres, distancias
    visitados.add(inicio)
    cola = collections.deque()
    cola.append(inicio)
    while(cola): 
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados: 
                padres[w] = v 
                distancias[w] = distancias[v] + 1 
                visitados.add(w)
                cola.append(w)
                if w == fin: 
                    return padres, distancias
    return padres, distancias

def cantidad_en_rango(grafo, vertice, n):
    '''Esta funcion devuelve la cantidad de vertices que se encuentran exactamente a n de distancia del vertice pasado por parametro'''
    if n<0:
        return 0
    visitados = set() 
    distancias = {} 
    cantidad = 0    
    visitados.add(vertice)
    distancias[vertice] = 0
    cola = collections.deque()
    cola.append(vertice)
    while(cola):
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                distancias[w] = distancias[v] + 1
                visitados.add(w)
                if distancias[w] < n: 
                    cola.append(w)
                else:
                    cantidad += 1  
    return cantidad


def backtracking(grafo, origen, vertice, n, camino):
    '''Algoritmo llamado en buscar_ciclo'''
    if((len(camino) == n+1) and (vertice == origen)):
        return True, camino
    for adyacente in grafo.adyacentes(vertice):
        if (adyacente != origen):
            if adyacente in camino:
                continue
        if (adyacente == origen):
            if len(camino) != n:
                continue
        if len(camino) > n:
            return False, camino
        camino.append(adyacente)
        booleano, camino = backtracking(grafo, origen, adyacente, n, camino)
        if booleano == False: 
            camino.remove(adyacente)
        else:
            return True, camino
    return False, camino

def buscar_ciclo(grafo, origen, n):
    '''Esta funcion se encarga de buscar un ciclo de n vertices que comience y termine en el vertice pasado por parametro'''
    camino = []
    camino.append(origen)
    return backtracking(grafo, origen, origen, n, camino)


def pageRank_personalizado(grafo, v, n, rol = None):
    '''Calcula el pagerank personalizado de un grafo'''
    valores_vertices = {}
    grados_vertices = grafo.obtener_grado_vertices()
    acumulador = 1
    for i in range(n*n):
        w = random.choice(grafo.adyacentes(v))
        acumulador *= (1 / grados_vertices[v])
        valores_vertices[w] =  acumulador 
        v = w
    return valores_vertices
 
def coeficiente_clustering_promedio(grafo):
    '''Calcula el clustering promedio de un grafo'''
    sumatoria_de_coeficientes = 0
    for vertice in grafo.obtener_vertices():
        sumatoria_de_coeficientes += coeficiente_clustering(grafo, vertice)
    return sumatoria_de_coeficientes/len(grafo.obtener_vertices())
        

def coeficiente_clustering(grafo, vertice):
    '''Calcula el coeficiente de clustering a partir de un vertice en particular'''
    adyacentes = grafo.adyacentes(vertice)
    grado_vertices = grafo.obtener_grado_vertices()
    if(len(adyacentes) < 2):
        return 0
    contador = 0
    total_adyacentes = len(adyacentes)
    visitados = set()
    for i in adyacentes:
        for j in adyacentes:
            if i == j:
                continue 
            if ((i, j) in visitados) or ((j, i) in visitados):
                continue
            visitados.add((i, j)) 
            if grafo.estan_unidos(i, j):
                contador += 1
    numerador = 2 * contador
    denominador = grado_vertices[vertice] * (grado_vertices[vertice] - 1)
    return numerador / denominador 
    
def suma_pageranks(grafo, lista_de_adyacentes, diccionario_pageranks):
    sumatoria = 0
    grados = grafo.obtener_grado_vertices()
    for vertice in lista_de_adyacentes:
        grado_vertice = grados[vertice]
        sumatoria += diccionario_pageranks[vertice]/grado_vertice
    return sumatoria

def pagerank(grafo, rol = None):
    '''Permite calcular el pagerank de un grafo. Se puede pasar opcionalmente
    un rol como parametro, que sirve como filtro, para 'pagerankear' unicamente
    el tipo de vertice de interes en el grafo. Sin embargo, el calculo se hace 
    sobre todo el grafo'''
    diccionario_pageranks = {}
    acumulador = ((1 - D)/len(grafo))
    for vertice in grafo.obtener_vertices():
        diccionario_pageranks[vertice] = 0
    for c in range(50): 
        for v in grafo.obtener_vertices(): 
            diccionario_pageranks[v] = acumulador + D * suma_pageranks(grafo, grafo.adyacentes(v), diccionario_pageranks)
    diccionario_filtrado = {}
    for elemento in diccionario_pageranks:
        if grafo.obtener_rol(elemento) == rol:
            diccionario_filtrado[elemento] = diccionario_pageranks[elemento]
    return diccionario_filtrado
