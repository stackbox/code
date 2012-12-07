"Modulo base para la creacion de escenas."

class Escena:
    "Esqueleto para cada una de las escenas del videojuego."
    def __init__(self):
        self.escena = self
    
    def eventos(self, teclado= None):
        "Leer los eventos para interactuar con los objetos."
        pass
    
    def actualizar(self):
        "Actualizar los objetos en la pantalla."
        pass
    
    def dibujar(self, pantalla):
        "Dibuja los objetos en la pantalla."
        pass
        
    def cambiar_escena(self, escena):
        "Cambia la escena del juego"
        self.escena = escena
