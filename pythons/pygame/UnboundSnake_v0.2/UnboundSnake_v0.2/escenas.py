"Escenas del juego."

from random import randrange
import pygame as p
from pygame.locals import K_F5
from comun import cargar_imagen, WIDTH, HEIGHT, Texto, Multilinea
from escena import Escena

class Serpiente(p.sprite.Sprite):
    "Define el comportamiento y caracteristicas de la serpiente."
    def __init__(self):
        "Inicializa la serpiente"
        p.sprite.Sprite.__init__(self)
        self.image = cargar_imagen("cuadro.png", True)
        self.rect = self.image.get_rect()
        self.direccion = 2
        self.cuerpo = []
        self.pos_x = 0
        self.pos_y = 0
        self.init_cuerpo()

    def init_cuerpo(self):
        "Crea el cuerpo de la serpiente y lo posiciona."
        pos_x = WIDTH / 2
        pos_y = HEIGHT / 2
        for i in range(0, 4):
            self.cuerpo.append(self.rect)
            self.cuerpo[i] = self.cuerpo[i].move(pos_x, pos_y)
            pos_y -= self.rect.h
        self.pos_x = pos_x
        self.pos_y = pos_y
            
    def teclado(self, evento):
        "Detecta los eventos del teclado para mover a la serpiente."
        if evento:
            tecla = evento[0].key - 272
            if 7 > (tecla + self.direccion) > 3:
                self.direccion = tecla

    def actualizar(self):
        "Actualiza la posicion de la serpiente en base a la direccion."
        if self.direccion == 2:
            self.pos_y += self.rect.h
        elif self.direccion == 1:
            self.pos_y -= self.rect.h
        elif self.direccion == 3:
            self.pos_x += self.rect.w
        elif self.direccion == 4:
            self.pos_x -= self.rect.w
        #Agregar nuevo elemento hacia la direccion indicada.
        self.cuerpo.insert(0, self.rect)
        self.cuerpo[0] = self.cuerpo[0].move(self.pos_x, self.pos_y)
        
    def se_alimento(self, comida):
        "Detecta si llego al alimento."
        if self.pos_x == comida.rect.x and self.pos_y == comida.rect.y:
            return True
        self.cuerpo.pop()
        return False
        
    def colisiona(self):
        "Verifica si hubo colision con alguna pared o consigo misma."
        if (self.cuerpo[0].left< 0 or self.cuerpo[0].right> WIDTH or
                self.cuerpo[0].top< 0 or self.cuerpo[0].bottom> HEIGHT or
                self.cuerpo[0] in self.cuerpo[1:]):
            return True
        return False



class Comida(p.sprite.Sprite):
    "Define la imagen de la comida y los lugares donde se encontrara."
    def __init__(self, serpiente):
        "Inicializa la comida."
        p.sprite.Sprite.__init__(self)
        #Cargar la imagen de la comida.
        self.image = cargar_imagen("comida.png", True)
        #Obtener las dimensiones de la comida.
        self.rect = self.image.get_rect()
        #Generar una comida.
        self.generar(serpiente)
        
    def generar(self, serpiente):
        "Genera nuevo alimento."
        while self.rect in serpiente.cuerpo:
            self.rect.left = randrange(0, WIDTH, self.rect.w)
            self.rect.top = randrange(0, HEIGHT, self.rect.h)
        
    def mostrar(self):
        "Sirve para regresar las coordenadas de la comida."
        return self.rect



class EscenaTitulo(Escena):
    "Escena inicial para desplegar menu."
    def __init__(self):
        Escena.__init__(self)
        self.fondo = cargar_imagen("titulo.jpg")
        self.txt_salir = Texto("[ESC] Salir", 48)
        self.txt_salir.pos(2, 2)
        self.txt_jugar = Texto("[F5] Jugar", 48)
        
    def eventos(self, teclado = None):
        "Leer eventos para determinar la escena siguiente."
        if teclado:
            tecla = teclado[0].key
            if tecla == K_F5:
                self.cambiar_escena(EscenaJuego())
        
    def dibujar(self, pantalla):
        "Dibujar el menu principal del videojuego."
        pantalla.blit(self.fondo, (0, 0))
        pantalla.blit(self.txt_salir.mostrar(), self.txt_salir.pos(2, 2, 0, 0))
        pantalla.blit(self.txt_jugar.mostrar(), self.txt_jugar.pos(2, 2, 0, 64))



class EscenaJuego(Escena):
    "Escena del juego."
    def __init__(self):
        Escena.__init__(self)
        #Creacion de objetos del videojuego.
        self.serpiente = Serpiente()
        self.comida = Comida(self.serpiente)
        #Variables de control.
        self.puntos = 0
        self.termino = False
        #Textos.
        self.puntuacion = Texto("Puntos: ")
                        
    def eventos(self, teclado = None):
        self.serpiente.teclado(teclado)
        
    def actualizar(self):
        self.serpiente.actualizar()
        if self.serpiente.se_alimento(self.comida):
            self.comida.generar(self.serpiente)
            self.puntos += 10
        if self.serpiente.colisiona():
            self.cambiar_escena(EscenaJuegoTerminado(self.puntos))
        
    def dibujar(self, pantalla):
        "Muestra los objetos en pantalla."
        pantalla.fill( (0x11, 0x11, 0x11) )        
        #Dibujar objetos en la interfaz.
        pantalla.blit(self.comida.image, self.comida.mostrar())
        pantalla.blit(self.puntuacion.mostrar(str(self.puntos)), 
            self.puntuacion.pos(horz= 0, vert= 0))
        #Dibujar la serpiente.
        for i in range(0, len(self.serpiente.cuerpo)):
            pantalla.blit(self.serpiente.image, self.serpiente.cuerpo[i])



class EscenaJuegoTerminado(Escena):
    "Escena ejeutada tras perder el juego."
    def __init__(self, puntos):
        "Inicializar Escena de Juego Terminado."
        Escena.__init__(self)
        self.fondo = cargar_imagen("terminado.jpg")
        self.instrucciones = Multilinea( ("Reiniciar [F5]", "Salir [Esc]"))
        self.instrucciones.pos(2, 2, 16, 16)
        self.terminado = Texto("Juego Terminado", tamano= 72)
        self.puntos = Texto("Puntos: " + str(puntos), tamano= 48)
        
    def eventos(self, teclado= None):
        "Redirecciona a la pantalla adecuada."
        if teclado:
            if teclado[0].key == K_F5:
                self.cambiar_escena(EscenaJuego())

    def dibujar(self, pantalla):
        "Mostrar pantalla de juego terminado."
        pantalla.blit(self.fondo, (0, 0))
        self.instrucciones.mostrar(pantalla, 2)
        pantalla.blit(self.terminado.mostrar(), 
            self.terminado.pos(1, 1, 0, -24))
        pantalla.blit(self.puntos.mostrar(), self.puntos.pos(1, 1, 0, 24))
