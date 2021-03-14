#!/usr/bin/python3

import csv
import sys
from grafo import Grafo
import grafo_utils
import random


INV_CANC = "Tanto el origen como el destino deben ser canciones"
NO_RTA = "No se encontro recorrido"

def conversor_camino_minimo(grafo_canciones_usuarios, cancion1, cancion2, diccionario_padres_camino):
    '''Recibe un diccionario que representa el resultado de comando_camino. Lo convierte en una lista ordenada'''
    camino_minimo = []
    camino_minimo.append(cancion2)
    actual = cancion2
    while actual != cancion1:
        padre = diccionario_padres_camino[actual]
        camino_minimo.append(padre)
        actual = padre 
    camino_minimo.reverse()  
    return camino_minimo 

def comando_camino(grafo_canciones_usuarios, cancion1, cancion2):
    '''Ejecuta el comando camino'''
    if not grafo_canciones_usuarios.vertice_pertenece(cancion1) or not grafo_canciones_usuarios.vertice_pertenece(cancion2):
        print(INV_CANC)
        return
    if grafo_canciones_usuarios.obtener_rol(cancion1) != 'cancion' or grafo_canciones_usuarios.obtener_rol(cancion2) != 'cancion':
        print(INV_CANC)
        return
    diccionario_padres_camino, distancias = grafo_utils.camino_minimo_bfs(grafo_canciones_usuarios, cancion1, cancion2)
    if cancion2 not in diccionario_padres_camino:
        print(NO_RTA)
        return
    camino_minimo = conversor_camino_minimo(grafo_canciones_usuarios, cancion1, cancion2, diccionario_padres_camino)
    for i in range(len(camino_minimo)):
        if grafo_canciones_usuarios.obtener_rol(camino_minimo[i]) == 'cancion':
            if i != (len(camino_minimo) - 1):
                playlist = grafo_canciones_usuarios.peso_arista(camino_minimo[i], camino_minimo[i+1])
                print(f"{camino_minimo[i]} --> aparece en playlist --> {playlist}", end= " ")
            else:
                print(f"{camino_minimo[i]}", end= " ")
        if grafo_canciones_usuarios.obtener_rol(camino_minimo[i]) == 'usuario':
            playlist = grafo_canciones_usuarios.peso_arista(camino_minimo[i], camino_minimo[i+1])
            print(f"--> de --> {camino_minimo[i]} --> tiene una playlist --> {playlist} --> donde aparece -->", end= " ")
    print()
    return

def comando_mas_importantes(grafo, n):
    '''Ejecuta el comando mas_importantes'''
    diccionario_pageranks = grafo_utils.pagerank(grafo, 'cancion')
    lista_ordenada_pageranks = sorted(diccionario_pageranks.items(), key=lambda x: x[1], reverse=True)
    return lista_ordenada_pageranks

def mostrar_mas_importantes(lista_ordenada_pageranks, n):
    '''Muestra por pantalla las canciones mas importantes'''
    lista = lista_ordenada_pageranks[:n+1]
    for i in range(n-1):
        print(f'{lista[i][0]}; ', end= "")   
    print(f'{lista[n-1][0]}')
    return

def comando_recomendacion(grafo, tipo, n, lista_canciones):
    '''Ejecuta el comando recomendacion, en sus dos variaciones'''
    if tipo == 'canciones':
        tipo = 'cancion' 
    else:
        tipo = 'usuario'
    diccionario = {}
    for i in range(10*len(lista_canciones)):
        cancion_aleatoria = random.choice(lista_canciones)
        dic = grafo_utils.pageRank_personalizado(grafo, cancion_aleatoria, n)
        for elemento in dic: 
            if elemento not in diccionario:
                diccionario[elemento] = 0
            diccionario[elemento] += dic[elemento]
    lista_ordenada = sorted(diccionario.items(), key=lambda x: x[1], reverse=True)
    i = 0
    l = len(lista_ordenada)
    for t in range(l):
        if grafo.obtener_rol(lista_ordenada[t][0]) == tipo:
            if i != n-1:
                print(f'{lista_ordenada[t][0]}; ', end= "")
                i += 1
                continue
            print(f'{lista_ordenada[t][0]}')
            break
    return 
    
def comando_ciclo(grafo, n, cancion):
    '''Ejecuta el comando ciclo'''
    boolean, camino = grafo_utils.buscar_ciclo(grafo, cancion, n)
    if boolean == False:
        print(NO_RTA)
        return
    print(camino[0], end= " ")
    for i in range(1, len(camino)):
        print(f"--> {camino[i]}", end= " ")
    print()
    return

def procesar_grafo_canciones_usuarios(grafo, usuario, cancion, artista, playlist):
    '''Guarda los datos de los usuarios y las canciones en un grafo, uniendo a estos dos
    grupos de vertices si el usuario en cuestion tiene a esa cancion en al menos una playlist.
    El grafo será bipartito'''
    cancion_y_artista = f'{cancion} - {artista}'
    if(not grafo.vertice_pertenece(usuario)):
        grafo.agregar_vertice(usuario, 'usuario')
    if(not grafo.vertice_pertenece(cancion_y_artista)): 
        grafo.agregar_vertice(cancion_y_artista, 'cancion') 
    grafo.agregar_arista(usuario, cancion_y_artista, playlist)
        
def guardar_datos_playlists(cancion, artista, playlist, diccionario_de_playlists):
    '''Guarda los nombres de las canciones en un arreglo, y los nombres de las playlists en un diccionario,
    guardando como datos asociados las canciones que pertenecen a aquella playlist'''
    cancion_y_artista = f'{cancion} - {artista}'
    if playlist not in diccionario_de_playlists: 
        diccionario_de_playlists[playlist] = []
    diccionario_de_playlists[playlist].append(cancion_y_artista)


def procesar_grafo_canciones(grafo, diccionario_de_playlists):
    '''Procesa los datos almacenados en la lista de canciones y el diccionario de playlists, y los introduce 
    al grafo diseñado para almacenar canciones y conectarlas si coinciden en alguna playlist'''
    for playlist in diccionario_de_playlists:
        unir_canciones_misma_playlist(grafo, diccionario_de_playlists[playlist])
    
def unir_canciones_misma_playlist(grafo, lista_canciones_playlist):
    '''Crea una arista entre las canciones que pertenecen a una misma playlist, sobre el grafo de solo canciones'''
    for p in lista_canciones_playlist:
        if not grafo.vertice_pertenece(p):
            grafo.agregar_vertice(p)
        for c in lista_canciones_playlist:
            if not grafo.vertice_pertenece(c):
                grafo.agregar_vertice(c)
            if p == c or grafo.estan_unidos(p, c):
                continue
            grafo.agregar_arista(p, c)

def procesar_datos(ruta_archivo):
    '''Lee y procesa los datos del archivo recibido de tipo tsv'''
    grafo_canciones_usuarios = Grafo()
    diccionario_de_playlists = {}
    playlist_actual = None
    with open(ruta_archivo) as archivo:
        lector_tsv = csv.reader(archivo, delimiter="\t")
        lista_archivo = list(lector_tsv)
        header = lista_archivo[0]
        for _id, user_id, track_name, artist, playlist_id, playlist_name, genres in lista_archivo[1:]:
            procesar_grafo_canciones_usuarios(grafo_canciones_usuarios, user_id, track_name, artist, playlist_name)
            guardar_datos_playlists(track_name, artist, playlist_name, diccionario_de_playlists)
    return grafo_canciones_usuarios, diccionario_de_playlists

def obtener_indice(cadena):
    i = 0
    for caracter in cadena:
        if caracter == ' ':
            break
        i+=1
    return i      

def procesar_entrada(entrada, grafo_canciones_usuarios, grafo_canciones_compartidas):
    '''Procesa la entrada de cada uno de los posibles comandos del programa, 
    para luego llamar a las funciones encargadas de ejecutar cada uno'''

    if "camino" in entrada: 
        lista_entrada = entrada.split("camino ")
        cancion1, cancion2 = ("".join(lista_entrada[1:])).split(">>>>")
        comando_camino(grafo_canciones_usuarios, cancion1.strip(), cancion2.strip())

    if "ciclo" in entrada:  
        lista_entrada = entrada.split("ciclo ")
        lista_entrada = lista_entrada[1:]
        i = obtener_indice(lista_entrada[0]) 
        n = "".join(lista_entrada[0][:i])
        cancion = "".join(lista_entrada[0][i:])
        comando_ciclo(grafo_canciones_compartidas, int(n), cancion.strip())

    if "clustering" in entrada: 
        lista_entrada = entrada.split("clustering ")
        if(len(lista_entrada) == 1):
            print(round(grafo_utils.coeficiente_clustering_promedio(grafo_canciones_compartidas), 3))
        else:
            print(round(grafo_utils.coeficiente_clustering(grafo_canciones_compartidas, lista_entrada[1].strip()), 3))

    if "recomendacion" in entrada:
        lista_entrada = entrada.split()
        comando = lista_entrada[0]
        tipo = lista_entrada[1] 
        n = int(lista_entrada[2])
        total = " ".join(lista_entrada[3:]).split(">>>>")
        for i in range(len(total)):
            cancion = total[i].strip()
            total[i] = cancion
        comando_recomendacion(grafo_canciones_usuarios, tipo, n, total)

    if "rango" in entrada: 
        lista_entrada = entrada.split("rango ")
        i = 0
        for caracter in lista_entrada[1]:
            if caracter == ' ':
                break
            i+=1
        n = "".join(lista_entrada[1][:i])
        cancion = "".join(lista_entrada[1][i:])
        print(grafo_utils.cantidad_en_rango(grafo_canciones_compartidas, cancion.strip(), int(n)))



def main():

    grafo_canciones_usuarios, diccionario_de_playlists = procesar_datos(sys.argv[1])
    grafo_canciones_compartidas = Grafo()
    entrada = sys.stdin.readline()
    creo_rank = False 
    creo_grafo_canciones = False
    lista = []
    while(entrada != ''):
        if "mas_importantes" in entrada:
            lista_entrada = entrada.split()
            if not creo_rank:
                lista_pagerank = comando_mas_importantes(grafo_canciones_usuarios, int(lista_entrada[1]))
                mostrar_mas_importantes(lista_pagerank, int(lista_entrada[1]))
                lista = lista_pagerank
                creo_rank = True
            else:
                mostrar_mas_importantes(lista, int(lista_entrada[1]))
        if 'rango' in entrada or 'clustering' in entrada or 'ciclo' in entrada:
            if not creo_grafo_canciones:
                procesar_grafo_canciones(grafo_canciones_compartidas, diccionario_de_playlists)
                creo_grafo_canciones = True
        if not "mas_importantes" in entrada:
        	procesar_entrada(entrada, grafo_canciones_usuarios, grafo_canciones_compartidas)
        entrada = sys.stdin.readline() 
main()
