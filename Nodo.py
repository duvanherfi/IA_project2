import numpy as np

class Nodo:
    def __init__(self,entorno,tipo,utilidad,profundidad=0,padre=None):
        self.entorno = entorno
        self.tipo = tipo
        self.profundidad = profundidad
        self.utilidad = utilidad
        self.padre = padre

    def posc(self):
        pos_c = np.where(self.entorno == 2)
        return np.array([pos_c[0][0], pos_c[1][0]])

    def mover(self, direccion, pisando):
        # Copia del entorno
        hijo = np.copy(self.entorno)

        # 1->Up-Right, 2->Right-Up, 3->Right-Down, 4->Down-Right
        # 5->Down-Left, 6->Left-Down, 7->Left-Up, 8->Up-Left
        #La primera dirección siempre indica el mayor desplazamiento del caballo(2 casillas)
        #1->Up-Right
        if (direccion == 1):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i-2][j+1] = 2
                        hijo[i][j] = pisando
                        return hijo
        #2->Right-Up
        if (direccion == 2):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i-1][j+2] = 2
                        hijo[i][j] = pisando
                        return hijo
        #3->Right-Down
        if (direccion == 3):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i+1][j+2] = 2
                        hijo[i][j] = pisando
                        return hijo
        #4->Down-Right
        if (direccion == 4):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i+2][j+1] = 2
                        hijo[i][j] = pisando
                        return hijo
        #5->Down-Left
        if (direccion == 5):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i+2][j-1] = 2
                        hijo[i][j] = pisando
                        return hijo
        #6->Left-Down
        if (direccion == 6):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i+1][j-2] = 2
                        hijo[i][j] = pisando
                        return hijo
        #7->Left-Up
        if (direccion == 7):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i-1][j-2] = 2
                        hijo[i][j] = pisando
                        return hijo
        #8->Up-Left
        if (direccion == 8):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == 2):
                        hijo[i-2][j-1] = 2
                        hijo[i][j] = pisando
                        return hijo
                        
    def utilidad(self,limite):
        utilidad_max=0
        utilidad_min=0
        if (self.profundidad == limite):
            for i in range(len(self.entorno)):
                    for j in range(len(self.entorno)):
                        if (self.entorno[i][j] == 5):
                            utilidad_max +=1
                        if (self.entorno[i][j]==6):
                            utilidad_min +=1
            if (self.tipo == 1):
                return utilidad_max
            else:
                return utilidad_min
        else:
            if (self.tipo == 1):
                return utilidad_max-10000000
            else:
                return utilidad_min+10000000

    def profundidadAcumulada(self):
        if (self.padre == None):
            return self.profundidad
        else:
            return self.profundidad + self.padre.profundidadAcumulada()
