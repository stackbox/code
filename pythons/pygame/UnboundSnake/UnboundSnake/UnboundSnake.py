"Videojuego de la Serpiente realizado con Pygame."

from random import randrange
import pygame as p
from pygame.locals import K_F5
from comun import WIDTH, HEIGHT, PANTALLA, ARRIBA, ABAJO, IZQUIERDA, DERECHA
from comun import cargar_imagen, salir, Texto, Multilinea



class Serpiente(p.sprite.Sprite):
    "Define el comportamiento y caracteristicas de la serpiente."
    def __init__(self):
        "Inicializa la serpiente"
        p.sprite.Sprite.__init__(self)
        self.image = cargar_imagen("cuadro.png", True)
        self.rect = self.image.get_rect()
        self.direccion = ABAJO
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
        if self.direccion == ABAJO:
            self.pos_y += self.rect.h
        elif self.direccion == ARRIBA:
            self.pos_y -= self.rect.h
        elif self.direccion == DERECHA:
            self.pos_x += self.rect.w
        elif self.direccion == IZQUIERDA:
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



class UnboundSnake():
    "Videojuego de la Serpiente realizado con Pygame."
    def __init__(self):
        "Inicializa el videojuego."
        p.init()
        self.pantalla = p.display.set_mode(PANTALLA)
        p.display.set_caption("Unbound Snake")
        #Creacion de objetos del videojuego.
        self.serpiente = Serpiente()
        self.comida = Comida(self.serpiente)
        #Variables de control.
        self.puntos = 0
        self.termino = False
        #Textos.
        self.puntuacion = Texto("Puntos: ")
        self.instrucciones = Multilinea( ("Reiniciar [F5]", "Salir [Esc]"))
        self.instrucciones.pos(2, 2, 16, 16)
        
    def dibujar(self):
        "Muestra los objetos en pantalla."
        self.pantalla.fill( (0x11, 0x11, 0x11) )        
        #Dibujar objetos en la interfaz.
        self.pantalla.blit(self.comida.image, self.comida.mostrar())
        self.pantalla.blit(self.puntuacion.mostrar(str(self.puntos)), 
            self.puntuacion.pos(horz= 0, vert= 0))
        #Dibujar la serpiente.
        for i in range(0, len(self.serpiente.cuerpo)):
            self.pantalla.blit(self.serpiente.image, self.serpiente.cuerpo[i])
        #Juego Terminado
        if self.termino:
            self.instrucciones.mostrar(self.pantalla, 2)
            terminado = Texto("Juego Terminado", tamano= 72)
            self.pantalla.blit(terminado.mostrar(), terminado.pos(1, 1))
        p.display.flip()
    
    def reiniciar(self, teclado):
        "Reinicia el juego en caso de haber perdido."
        if teclado:
            if teclado[0].key == K_F5:
                self.__init__()
    
    def jugar(self):
        "Ejecuta el videojuego."
        jugando = True
        reloj = p.time.Clock()
        while jugando:
            #Frecuencia de actualizacion (Velocidad de la serpiente).
            reloj.tick(10)
            #Obtencion de eventos.
            teclado = p.event.get(p.KEYDOWN)
            cerrar  = p.event.get(p.QUIT)
            # Nucleo del juego. ########################################
            if not self.termino:
                #Control de la serpiente.
                self.serpiente.teclado(teclado)
                #Actualizar la posicion de la serpiente.
                self.serpiente.actualizar()
                #Generar nueva comida si la serpiente se alimento.
                if self.serpiente.se_alimento(self.comida):
                    self.comida.generar(self.serpiente)
                    self.puntos += 10
            else:
                self.reiniciar(teclado)
            if self.serpiente.colisiona():
                self.termino = True
            jugando = salir(cerrar, teclado)
            ############################################################
            self.dibujar()



if __name__ == '__main__':
    JUEGO = UnboundSnake()
    JUEGO.jugar()
