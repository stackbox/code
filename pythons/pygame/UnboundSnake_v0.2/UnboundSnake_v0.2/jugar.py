"Script para ejecutar el juego."

from director import Director
from escenas import EscenaTitulo

def main():
    "Ejecutar el juego."
    director = Director("Unbound Snake v0.2")
    director.ejecutar(EscenaTitulo(), 10)

if __name__ == "__main__":
    main()
