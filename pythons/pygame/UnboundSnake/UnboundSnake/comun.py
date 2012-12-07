"Funciones comunes utilizadas por los diversos juegos."

import os
import sys
import pygame as p
from pygame.locals import K_ESCAPE


WIDTH    = 640
HEIGHT   = 480
PANTALLA = (WIDTH, HEIGHT)

ARRIBA    = 1
ABAJO     = 2
DERECHA   = 3
IZQUIERDA = 4

def cargar_imagen(nombre, alpha= False, directorio= "imagenes"):
    "Carga una imagen del directorio predefinido."
    ruta = os.path.join(directorio, nombre)
    try:
        imagen = p.image.load(ruta)
    except:
        print("No se puede cargar la imagen: ", ruta)
        raise
        
    if alpha == True:
        imagen = imagen.convert_alpha()
    else:
        imagen = imagen.convert()
    return imagen



def salir(cerrar, teclado):
    "Define el fin del programa por medio de la tecla [Escape]."
    if cerrar:
        return False
    elif teclado:
        teclado = teclado[0]
        if teclado.key == K_ESCAPE:
            return False;
    return True



class Texto():
    "Crea un texto para mostrar en pantalla."
    def __init__(self, texto_predeterminado= "", fuente= None, tamano= 24):
        "Inicializa el texto."
        self.fuente = p.font.Font(fuente, tamano)
        self.default = texto_predeterminado
        self.texto = None
        self.rect = None
        self.mostrar()
        
    def mostrar(self, cadena= "", color= (0xFF, 0xFF, 0xFF) ):
        "Regresa el texto a mostrar."
        self.texto = self.fuente.render(self.default + cadena, True, color)
        self.rect = self.texto.get_rect()
        return self.texto
        
    def pos(self, horz= 0, vert= 0, offset_x= 0, offset_y= 0):
        "Obtiene la posicion en la cual se mostrara el texto."
        if vert == 0:
            self.rect.top = offset_y
        elif vert == 1:
            self.rect.centery = HEIGHT / 2 + offset_y
        elif vert == 2:
            self.rect.bottom = HEIGHT - offset_y
        
        if horz == 0:
            self.rect.left = offset_x
        elif horz == 1:
            self.rect.centerx = WIDTH / 2 + offset_x
        elif horz == 2:
            self.rect.right = WIDTH - offset_x
        return self.rect



class Multilinea():
    "Clase para mostrar varias lineas de texto."
    def __init__(self, lineas= (""), fuente= None, tamano= 24):
        "Inicializa los multiples textos."
        self.fuente = p.font.Font(fuente, tamano)
        self.lineas = lineas
        self.rect = p.Rect(0, 0, 0, 0)
        self.texto = []
        self.rects = []
        self.tamano = [0, 0]
        self.generar()
        
    def generar(self):
        "Genera un texto para cada cadena y el rectangulo contennedor."
        for linea in self.lineas:
            #Creando los nuevos textos y sus posiciones.
            self.texto.append(self.fuente.render(linea, True, (255, 255, 255)))
            self.rects.append(self.texto[-1].get_rect())
            #Creando el contenedor de todos los textos.
            if self.rects[-1].w > self.rect.w:
                self.rect.w = self.rects[-1].w
            self.rect.h += self.rects[-1].h

    def mostrar(self, pantalla, alinear= 0):
        "Muestra los textos en pantalla."
        for i in range(0, len(self.rects)):
            self.rects[i].top = self.rect.top + self.rects[i].h * i
            self.alineacion(alinear)
            pantalla.blit(self.texto[i], self.rects[i])
        
    def pos(self, horz= 0, vert= 0, offset_x= 0, offset_y= 0):
        "Define la posicion del contenedor en la pantalla."
        if vert == 0:
            self.rect.top = offset_y
        elif vert == 1:
            self.rect.centery = HEIGHT / 2 + offset_y
        elif vert == 2:
            self.rect.bottom = HEIGHT - offset_y
        if horz == 0:
            self.rect.left = offset_x
        elif horz == 1:
            self.rect.centerx = WIDTH / 2 + offset_x
        elif horz == 2:
            self.rect.right = WIDTH - offset_x

    def alineacion(self, alinear= 0):
        "Define la alineacion de cada texto respecto al contenedor."
        for rect in self.rects:
            if alinear == 0:
                rect.left = self.rect.left
            elif alinear == 1:
                rect.centerx = self.rect.centerx
            elif alinear == 2:
                rect.right = self.rect.right
