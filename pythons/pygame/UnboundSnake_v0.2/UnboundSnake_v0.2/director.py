"Modulo para gestion de escenas en Pygame."

import pygame as p
from pygame.locals import K_ESCAPE
from comun import PANTALLA

def salir(cerrar, teclado):
    "Define el fin del programa por medio de la tecla [Escape]."
    if cerrar:
        return False
    elif teclado:
        teclado = teclado[0]
        if teclado.key == K_ESCAPE:
            return False
    return True


class Director():
    "Clase para gestionar escenas."
    def __init__(self, titulo= ""):
        "Inicializar Pygame."
        p.init()
        self.pantalla = p.display.set_mode(PANTALLA)
        p.display.set_caption(titulo)
        self.escena = None
        self.reloj = p.time.Clock()
        
    def ejecutar(self, escena_inicial, fps= 60):
        "Ejecuta la logica del juego."
        self.escena = escena_inicial
        jugando = True
        while jugando:
            self.reloj.tick(fps)
            #Adquisicion de eventos.
            cerrar  = p.event.get(p.QUIT)
            teclado = p.event.get(p.KEYDOWN)
            #Interaccion con la escena.
            self.escena.eventos(teclado)
            self.escena.actualizar()
            self.escena.dibujar(self.pantalla)
            #Cambio de escena
            self.escena = self.escena.escena
            #Salir del juego.
            jugando = salir(cerrar, teclado)
            p.display.flip()
