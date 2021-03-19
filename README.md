# Recomendacion-de-Canciones-en-Spotify

# Objetivo

Modelación de un sistema de recomendación sobre un sistema de streaming de música: las canciones, playlists y usuarios.
Nos interesa modelar y entender cómo están compuestas las playlists, si un usuario y otro son similares, poder recomendar canciones o playlists enteras.
El contenido mostrado a continuacion fue extraido del trabajo que nos entregaron los profesores de Algoritmos y Programación II para llevar acabo dicho proyecto.

# Datos Disponibles

Trabajaremos con una ínfima porción de datos obtenidos de una [competencia pública realizada por la plataforma Spotify en 2018](https://www.recsyschallenge.com/2018/). 
Cuenta con cerca de 2 millones de entradas. Pueden encontrar el archivo ya procesado aquí. El formato del archivo es tsv:

```
ID	USER_ID	TRACK_NAME	ARTIST	PLAYLIST_ID	PLAYLIST_NAME	GENRES
1	sitevagalume	Eraser	Ed Sheeran	6736120	Ed Sheeran - Divide	Pop,Rock,Pop/Rock
2	sitevagalume	Castle On The Hill	Ed Sheeran	6736120	Ed Sheeran - Divide	Pop,Rock,Pop/Rock
3	sitevagalume	Dive	Ed Sheeran	6736120	Ed Sheeran - Divide	Pop,Rock,Pop/Rock
...
3251	sapatini	Não Foi Em Vão	Sorriso Maroto	1169827	\o/	Romântico,Pagode,Samba
3252	sapatini	Não Mereço Ser Amante	Sorriso Maroto	1169827	\o/	Romântico,Pagode,Samba
...
```

* ID: id de la entrada
* USER_ID: Id del usuario que creó la playlist en cuestión.
* TRACK_NAME: nombre de la canción
* ARTIST: nombre del artista (o grupo), compositor/a de la canción.
* PLAYLIST_ID: id de la playlist en la que se encuentra esta canción (no necesariamente una canción pertenece a una sóla playlist; algo muy improbable)
* PLAYLIST_NAME: nombre de la playlist.
* GENRES: géneros a los que pertenece la canción (separados por coma)

A continuación se listarán los comandos junto a ejemplos de entrada y salidas para el caso de la red reducida.

### Camino más corto

* Comando: camino.
* Parámetros: origen y destino (separados por >>>>). Origen y destino son canciones. Se indica el autor en cada caso.
* Utilidad: nos imprime una lista con la cual se conecta (en la menor cantidad de pasos posibles) una canción con otra, considerando los usuarios intermedios y las listas de reproducción en las que aparecen.
* Ejemplos: Entrada:

```
  camino Don't Go Away - Oasis >>>> Quitter - Eminem
  camino yarits >>>> Quitter - Eminem
  camino Oops!...I Did It Again - Britney Spears >>>> Love Story - Taylor Swift
  camino Mr. Brightside - The Killers >>>> Grow Old With Me - Tom Odell
```
Salida:

```
Don't Go Away - Oasis --> aparece en playlist --> misturo tudãao ;x --> de --> 8902446 --> tiene una playlist --> sóo nacionais' --> donde aparece --> Ela Vai Voltar (Todos Os Defeitos de Uma Mulher Perfeita) - Charlie Brown Jr --> aparece en playlist --> Playlist da Yara --> de --> yarits --> tiene una playlist --> Playlist da Yara --> donde aparece --> Quitter - Eminem
  Tanto el origen como el destino deben ser canciones
  Oops!...I Did It Again - Britney Spears --> aparece en playlist --> Britney Spears --> de --> aline_hdb --> tiene una playlist --> Só Antigas --> donde aparece --> I Will Always Love You - Whitney Houston --> aparece en playlist --> romaticas --> de --> joyce9224 --> tiene una playlist --> musicas --> donde aparece --> Love Story - Taylor Swift
  No se encontro recorrido
```

### Canciones más importantes

Utilizaremos el algoritmo de [PageRank](https://algoritmos-rw.github.io/algo2/material/apuntes/pagerank/) para implementar este comando, para determinar cuáles son la canciones más importantes.

* Comando: mas_importantes.
* Parámetros: n, la cantidad de canciones más importantes a mostrar.
* Utilidad: nos muestra las n canciones más centrales/importantes del mundo según el algoritmo de pagerank, ordenadas de mayor importancia a menor importancia. También se puede utilizar otra métrica/algoritmo para detectar esto, como [Hubs and Authorities](https://es.wikipedia.org/wiki/Algoritmo_HITS) ([paper original aquí](https://www.cs.cornell.edu/home/kleinber/auth.pdf)).
* Ejemplo: Entrada:

```
  mas_importantes 20
```
Salida:

```
Bad Romance - Lady Gaga; Poker Face - Lady Gaga; Telephone (feat. Beyoncé) - Lady Gaga; Paparazzi - Lady Gaga; Halo - Beyoncé; Viva La Vida - Coldplay; Single Ladies (Put a Ring on It) - Beyoncé; Decode - Paramore; In The End - Linkin Park; Levo Comigo - Restart; Leave Out All The Rest - Linkin Park; Broken-Hearted Girl - Beyoncé; Alejandro - Lady Gaga; If I Were A Boy - Beyoncé; I Gotta Feeling - Black Eyed Peas; Amo Noite E Dia - Jorge e Mateus; Sweet Dreams - Beyoncé; Smells Like Teen Spirit - Nirvana; Wonderwall - Oasis; Just Dance (feat. Colby O'Donis) - Lady Gaga
```

### Recomendación (usuarios o canciones)

Usando la idea de [PageRank Personalizado](https://algoritmos-rw.github.io/algo2/material/apuntes/pagerank/), y lo indicado en [este paper](http://web.stanford.edu/class/msande233/handouts/lecture8.pdf), implementaremos un algoritmo que permita determinar qué otros usuarios se puede recomendar seguir, o bien qué canciones probablemente pudieran gustar, a partir de un listado de canciones.

* Comando: recomendacion.
* Parámetros: usuarios/canciones, si se espera una recomendación para seguir un usuario o para escuchar una cancion; n, la cantidad de usuarios o canciones a recomendar; cancion1 >>>> cancion2 >>>> ... >>>> cancionK, las canciones que ya sabemos que le gustan a la persona a recomendar.
* Utilidad: Dar una lista de n usuarios o canciones para recomendar, dado el listado de canciones que ya sabemos que le gustan a la persona a la cual recomedar.
* Ejemplo: Entrada:

```
  recomendacion canciones 10 Love Story - Taylor Swift >>>> Toxic - Britney Spears >>>> I Wanna Be Yours - Arctic Monkeys >>>> Hips Don't Lie (feat. Wyclef Jean) - Shakira >>>> Death Of A Martian - Red Hot Chili Peppers
  recomendacion usuarios 5 Love Story - Taylor Swift >>>> Toxic - Britney Spears >>>> I Wanna Be Yours - Arctic Monkeys >>>> Hips Don't Lie (feat. Wyclef Jean) - Shakira >>>> Death Of A Martian - Red Hot Chili Peppers
```

Salida:

```
Butterfly - Grimes; Cola - Lana Del Rey; In Time - FKA Twigs; Touch - Troye Sivan; Hurricane - 30 Seconds To Mars; Boring - The Pierces; Cut Your Teeth - Kyla La Grange; Earned It - The Weeknd; Player (Feat. Chris Brown) - Tinashe; If I Were A Boy - Beyoncé
  lorenafazion; naosoumodinha; hlovato906gmail; tiagogabbana19; extralouca
  
```
 
### Ciclo de n canciones

* Comando: ciclo.
* Parámetros: n y cancion.
* Utilidad: permite obtener un ciclo de largo n (dentro de la red de canciones) que comience en la canción indicada.
* Ejemplo: Entrada:

```
ciclo 7 By The Way - Red Hot Chili Peppers
  ciclo 15 Love Me Like You Do - Ellie Goulding
```

Salida:

```
By The Way - Red Hot Chili Peppers --> Fairy Tale - Shaman --> I Hate Everything About You - Three Days Grace --> Viva La Vida - Coldplay --> Under The Bridge - Red Hot Chili Peppers --> November Rain - Guns N' Roses --> Cryin' - Aerosmith --> By The Way - Red Hot Chili Peppers
  Love Me Like You Do - Ellie Goulding --> Uptown Funk (Feat. Bruno Mars) - Mark Ronson --> Thinking Out Loud - Ed Sheeran --> Ship To Wreck - Florence And The Machine --> Fourfiveseconds (feat. Kanye West, Paul Mccartney) - Rihanna --> Feeling Myself (Feat. Beyoncé) - Nicki Minaj --> Cheerleader (Felix Jaehn Remix) - Omi --> Ayo (Feat. Tyga) - Chris Brown --> Um Leão - Pitty --> I Know What You Did Last Summer (feat. Camila Cabello) - Shawn Mendes --> Hello - Adele --> Confident - Demi Lovato --> Hotline Bling - Drake --> My House - Flo Rida --> Alive - Sia --> Love Me Like You Do - Ellie Goulding

```

### Todas en Rango

* Comando: rango.
* Parámetros: n y cancion.
* Utilidad: permite obtener la cantidad de canciones que se encuenten a exactamente n saltos desde la cancion pasada por parámetro.
* Ejemplo: Entrada:

```
  rango 8 Shots - Imagine Dragons
  rango 3 Shots - Imagine Dragons
  rango 2 After Dark - Asian Kung-fu Generation
  rango 4 I'm Yours - Jason Mraz
```

Salida:
```
  0
  10325
  0
  431
```

### Coeficiente de Clustering


* Comando: clustering
* Parámetros: cancion, opcional.
* Utilidad: Permite obtener el coeficiente de clustering de la canción indicada. En caso de no indicar canción, se deberá informar el clustering promedio de la red. En ambos casos, informar con hasta 3 dígitos decimales.
* Ejemplo: Entrada:

```
  clustering Teenage Dream - Katy Perry
  clustering Grow Old With Me - Tom Odell
  clustering Drag Me Down - One Direction
  clustering Heart Attack - Demi Lovato
  # Ejemplo con red reducida de 5.000 entradas
  clustering
```

Salida:

```
  0.244
  0.000
  0.605
  1.000
  # Ejemplo con red reducida de 5.000 entradas
  0.988
  
```
# Colaboracion
El desarrollo de este trabajo fue hecho en conjunto con Tomás Bernardotti.

