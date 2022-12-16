import numpy as np

class Nodo:
    def __init__(self,entorno,tipo,utilidad=-1000000,profundidad=0,padre=None):
        self.entorno = entorno
        self.tipo = tipo
        self.profundidad = profundidad
        self.utilidad = utilidad
        self.padre = padre

    def posc(self):
        if (self.tipo == 1):
            pos_c = np.where(self.entorno == 2)
        else:
            pos_c = np.where(self.entorno == 1)
        return np.array([pos_c[0][0], pos_c[1][0]])

    def mover(self, direccion, pisando):
        # Copia del entorno
        hijo = np.copy(self.entorno)

        # 1->Up-Right, 2->Right-Up, 3->Right-Down, 4->Down-Right
        # 5->Down-Left, 6->Left-Down, 7->Left-Up, 8->Up-Left
        #La primera dirección siempre indica el mayor desplazamiento del caballo(2 casillas)
        #1->Up-Right
        if (self.tipo == 1):
            caballo = 2
        else:
            caballo=1
        if (direccion == 1):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == caballo):
                        hijo[i-2][j+1] = caballo
                        hijo[i][j] = pisando
                        return hijo
        #2->Right-Up
        if (direccion == 2):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == caballo):
                        hijo[i-1][j+2] = caballo
                        hijo[i][j] = pisando
                        return hijo
        #3->Right-Down
        if (direccion == 3):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == caballo):
                        hijo[i+1][j+2] = caballo
                        hijo[i][j] = pisando
                        return hijo
        #4->Down-Right
        if (direccion == 4):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == caballo):
                        hijo[i+2][j+1] = caballo
                        hijo[i][j] = pisando
                        return hijo
        #5->Down-Left
        if (direccion == 5):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == caballo):
                        hijo[i+2][j-1] = caballo
                        hijo[i][j] = pisando
                        return hijo
        #6->Left-Down
        if (direccion == 6):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == caballo):
                        hijo[i+1][j-2] = caballo
                        hijo[i][j] = pisando
                        return hijo
        #7->Left-Up
        if (direccion == 7):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == caballo):
                        hijo[i-1][j-2] = caballo
                        hijo[i][j] = pisando
                        return hijo
        #8->Up-Left
        if (direccion == 8):
            for i in range(len(hijo)):
                for j in range(len(hijo[i])):
                    if (hijo[i][j] == caballo):
                        hijo[i-2][j-1] = caballo
                        hijo[i][j] = pisando
                        return hijo
                        
    def setUtilidad(self,limit):
        utilidad_max=0
        utilidad_min=0
        if (self.profundidadAcumulada() == limit):
            for i in range(len(self.entorno)):
                for j in range(len(self.entorno[i])):
                    if (self.entorno[i][j] == 4):
                        utilidad_max +=1
                    if (self.entorno[i][j]==5):
                        utilidad_min +=1
            if (self.tipo == 1):
                self.utilidad=utilidad_max
            else:
                self.utilidad=utilidad_min
        else:
            if (self.tipo == 1):
                self.utilidad=utilidad_max-10000000
            else:
                self.utilidad=utilidad_min+10000000

    def profundidadAcumulada(self):
        if (self.padre == None):
            return self.profundidad
        else:
            return self.profundidad + self.padre.profundidadAcumulada()

    def aplicarBono(self,pos,_color):
        colorear_izq = pos[1]-1
        colorear_der = pos[1]+1
        colorear_arr = pos[0]-1
        colorear_aba = pos[0]+1
        #Validar izquierda
        if colorear_izq >= 0:
            if self.entorno[pos[0]][colorear_izq] == 0:
               self.entorno[pos[0]][colorear_izq]=_color
        #Validar derecha
        if colorear_der <= len(self.entorno[0])-1:
             if self.entorno[pos[0]][colorear_der] == 0:
                self.entorno[pos[0]][colorear_der]=_color
        #Validar arriba
        if colorear_arr >= 0:
            if self.entorno[colorear_arr][pos[1]] == 0:
               self.entorno[colorear_arr][pos[1]]=_color
        #Validar abajo
        if colorear_aba <= len(self.entorno) - 1:
            if self.entorno[colorear_aba][pos[1]] ==0:
               self.entorno[colorear_aba][pos[1]]=_color
