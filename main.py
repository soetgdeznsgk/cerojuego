from pynput import keyboard
from pynput.keyboard import Key
from time import sleep
from os import system, name, _exit

import random as ran


#   Inicializa el modulo keyboard
keyboard_controller = keyboard.Controller()

x = "."         # Diseño del terreno baldío
o = "\033[1m\033[31m0\033[0m"   # Código Unicode para colorear el str 

numeros = ["\033[1m" + "\033[0;31m" + "1\033[0m", 
           "\033[1m" + "\033[0;32m" + "2\033[0m", 
           "\033[1m\033[0;33m3\033[0m", 
           "\033[1m\033[0;34m4\033[0m", 
           "\033[1m\033[0;35m5\033[0m", 
           "\033[1m\033[0;36m6\033[0m", 
           "\033[1m" + "\033[67m" + "7\033[0m", 
           "\033[1m" + "\033[38m" + "8\033[0m", 
           "\033[1m" + "\033[93m9\033[0m"]


# Para borrar la terminal

def  clear(): 
  if name == "nt":
    system("cls")
  else:
    system("clear")



# Generar un mapa cuadrado de entre 4 y 10 x's de dimensión

def  generar_mapa() -> list:    
  global o
  global x
  
  dimension = ran.randint(4, 7)
  mapa = []
  sublista = []
  for i in range(dimension):
    for c in range(dimension):
      sublista.append(x)       
    mapa.append(sublista)
    sublista = []

  return insertar_obstaculos(insertar_jugador(mapa, dimension), dimension)


#  Inserta al jugador en una posición aleatoria
  
def  insertar_jugador(mapa: list, dimension: int) -> list:
  global o
  x = int(ran.randint(0, dimension - 1))
  y = int(ran.randint(0, dimension - 1))
  mapa[x][y] = o

  return mapa


#  Imprime el mapa, con colores
  
def  imprimir_mapa(mapa: list) -> None:   
  for columna in mapa:
    for indice, elemento in enumerate(columna):
      print(f"{elemento}  ", end="")
      
      if indice == len(columna) - 1:
        print("\n", end="")


#  Devuelve las coordenadas de cualquier cosa que le pases como llave

def  encontrar(mapa: list, llave: int) -> list:
  for x, fila in enumerate(mapa):
    for y, posicion in enumerate(fila):
      if llave == posicion:
        return [x, y]
  return -1 


#  Convierte al jugador en lo que se coma, y le rellena la vida

def  comer_numeros(mapa: list, ubicacion: list, vida: int) -> str:
  global o
  global x
  
  if mapa[ubicacion[0]][ubicacion[1]] != x:
    o = mapa[ubicacion[0]][ubicacion[1]]
    return 11

  return vida


#  Mueve al jugador en la dirección indicada, pero sólo si no se encuentra con un número que no sea su misma identidad + 1
  
def  mover_jugador(mapa: list, jugador: str, vida: int) -> None:

  global o
  global x

  posicion = encontrar(mapa, o)
  direccion = {"arriba": [posicion[0] - 1, posicion[1]],
               "abajo": [posicion[0] + 1, posicion[1]], 
               "derecha": [posicion[0], posicion[1] + 1], 
               "izquierda": [posicion[0], posicion[1] -1],
               "ninguna": [posicion[0], posicion[1]]}
    
  llave_direccion: str

  def presionar(key):
        nonlocal llave_direccion    # Para que altere llave_direccion fuera de ésta función

        if key == Key.up:
            llave_direccion = "arriba"
        elif key == Key.down:
            llave_direccion = "abajo"
        elif key == Key.right:
            llave_direccion = "derecha"
        elif key == Key.left:
            llave_direccion = "izquierda"
        else:
            llave_direccion = "ninguna"
        return False    # Para que sólo registre un tecleo

  with keyboard.Listener(
    on_press=presionar,
    on_release = None
    ) as keyboard_Listener: # Objeto que activa el registro del teclado
    keyboard_Listener.join() # Ejecución del registro

  nueva_posicion = direccion[llave_direccion]


  

  if -1 not in nueva_posicion and len(mapa) not in nueva_posicion: # Función que revisa si ésta nueva ubicación es un número, y si sí lo es, cambia la skin del jugador

    print(mapa[nueva_posicion[0]][nueva_posicion[1]])
    
    if mapa[nueva_posicion[0]][nueva_posicion[1]] == x or int(mapa[nueva_posicion[0]][nueva_posicion[1]][9]) == int(o[9]) + 1:
      
      vida = comer_numeros(mapa, nueva_posicion, vida)
    
      mapa[nueva_posicion[0]][nueva_posicion[1]] = o  #Inserta al jugador a en la dirección indicada
    
      mapa[posicion[0]][posicion[1]] = x  #Elimina al jugador de su espacio anterior

  return vida


#  Reparte aleatoriamente los números del 1 al 9

def  insertar_obstaculos(mapa: list, dimension: int):
  
  global o, numeros, x

  while len(numeros) > 0:
    y = ran.randint(0, dimension - 1)
    xC = ran.randint(0, dimension - 1)

    if mapa[y][xC] == x:
      mapa[y][xC] = numeros.pop(0)

    else:
      continue

  return mapa
  


def  revisar_progreso(mapa: list) -> int:

  for x in range(1, 10):
    if encontrar(mapa, x) != -1:
      return

  return "Exito!"


  

def  main() -> None:
  global o
  global x
  vida = 10

  mapa = generar_mapa()

  print("Instrucciones:")
  sleep(1)
  print("Comienzas jugando como un \033[1m\033[31mcero\033[0m")
  sleep(1)
  print("Tienes que comerte al resto de \033[93mnúmeros\033[0m en \033[1morden\033[0m")
  sleep(1)
  print("Te mueves con las flechitas")
  sleep(1)
  print("\033[1mBuena suerte!\033[0m\n")
  
  while True: 
    print("Aliento:", " ".join(["❤" for x in range(vida)]))
    
    imprimir_mapa(mapa)
    vida = mover_jugador(mapa, o, vida)
    vida -= 1

    clear()
    
    if encontrar(mapa, "\033[1m" + "\033[38m" + "8\033[0m") == -1:
      imprimir_mapa(mapa)
      print("pudiste pasarte un juego injusto?, cómo??")
      break 

    elif vida < 1:
      imprimir_mapa(mapa)
      print("perdedor!")
      break
    
main()
