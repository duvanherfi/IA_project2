import numpy as np


class Nodo:
    def __init__(self, entorno, padre=None, profundidad=0, costo=0, estrella=0, flor=0, pisando=0):
        # • 0 ->  una casilla libre
        # • 1 ->  un muro
        # • 2 ->  punto donde inicia Mario
        # • 3 ->  una estrella
        # • 4 ->  una flor
        # • 5 ->  un koopa
        # • 6 ->  la princesa
        self.entorno = entorno
        self.padre = padre
        self.costo = costo
        self.estrella = estrella
        self.flor = flor
        self.pisando = pisando
        self.profundidad = profundidad

    def __str__(self):
        self.mostrar()

    def meta(self, posm, posp):
        if(posm == posp):
            return 1
        else:
            return 0

    def posm(self):
        pos_m = np.where(self.entorno == 2)
        return np.array([pos_m[0][0], pos_m[1][0]])

    def mostrar(self):
        print("La matriz es la siguiente:")
        for fila in self.entorno:
            for valor in fila:
                print("\t", valor, end=" ")
            print()

    def mover(self, direccion, pisando):
        # Copia del entorno
        hijo = np.copy(self.entorno)

        # 1->left, 2->Right, 3->Up, 4->Down
        if (direccion == 1):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i][j-1] = 2
                        hijo[i][j] = pisando
                        return hijo

        if (direccion == 2):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i][j+1] = 2
                        hijo[i][j] = pisando
                        return hijo

        if (direccion == 3):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i-1][j] = 2
                        hijo[i][j] = pisando
                        return hijo

        if (direccion == 4):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i+1][j] = 2
                        hijo[i][j] = pisando
                        return hijo

    def costoAcumulado(self):
        if (self.padre == None):
            return self.costo
        else:
            return self.costo + self.padre.costoAcumulado()

    def profundidadAcumulada(self):
        if (self.padre == None):
            return self.profundidad
        else:
            return self.profundidad + self.padre.profundidadAcumulada()

    def heuristica(self, goal):
        return sum(np.absolute(goal - self.posm()))/2
