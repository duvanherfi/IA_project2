from Nodo import Nodo,np
class Juego:
  profundidad = 0
  movimientos = []
  def __init__(self, dificultad, raiz):
    self.difucultad = dificultad
    self.raiz = Nodo(-1,5000)

  def minimax(self,arbol):
    profundidadNodos = [nodo.profundidad for nodo in arbol]
    indexMaxProfundidadNodo = profundidadNodos.index(max(profundidadNodos))
    nodo_expandido = arbol.pop(indexMaxProfundidadNodo)
    if nodo_expandido.padre is None:
        return nodo_expandido
    if nodo_expandido.padre.tipo == 1:
        if nodo_expandido.utilidad > nodo_expandido.padre.utilidad:
            nodo_expandido.padre.utilidad = nodo_expandido.utilidad
    else:
        if nodo_expandido.utilidad < nodo_expandido.padre.utilidad:
            nodo_expandido.padre.utilidad = nodo_expandido.utilidad
    return self.minimax(arbol)

  def crearArbol(self,nodo,limit_profundidad):
    _tipo = 0
    _color = 0
    #color = 5 -> verde, color=6->rojo
    #max = verde, min=rojo
    if nodo.tipo ==  1:
        _tipo = -1
        _color = 6
    else:
        _tipo = 1
        _color = 5
    if (self.profundidad > limit_profundidad):
        return self.movimientos
    else:
        self.profundidad +=1
        upright = [nodo.posc()[0]-2,nodo.posc()[1]+1]
        if upright[0] >= 0 and upright[1] <= len(nodo.entorno[0]) - 1:
            if nodo.entorno[upright[0]][upright[1]] == 0:
                self.movimientos.append(Nodo(nodo.mover(1,_color)),_tipo,nodo.utilidad(limit_profundidad),self.profundidad,nodo)

        rightup = [nodo.posc()[0]-1,nodo.posc()[1]+2]
        if rightup[1] <= len(nodo.entorno[0]) - 1 and rightup[0] >=0:
            if nodo.entorno[rightup[0]][rightup[1]] == 0:
                self.movimientos.append(Nodo(nodo.mover(2,_color)),_tipo,nodo.utilidad(limit_profundidad),self.profundidad,nodo)
         
        rightdown = [nodo.posc()[0]+1,nodo.posc()[1]+2]
        if rightdown[1] <= len(nodo.entorno[0])-1 and rightdown[0] <= len(nodo.entorno) - 1:
            if nodo.entorno[rightdown[0]][rightdown[1]] == 0:
                self.movimientos.append(Nodo(nodo.mover(3,_color)),_tipo,nodo.utilidad(limit_profundidad),self.profundidad,nodo)

        downright = [nodo.posc()[0]+2,nodo.posc()[1]+1]
        if downright[0] <= len(nodo.entorno) - 1 and downright[1] <= len(nodo.entorno[0])-1:
            if nodo.entorno[downright[0]][downright[1]] == 0:
                self.movimientos.append(Nodo(nodo.mover(4,_color)),_tipo,nodo.utilidad(limit_profundidad),self.profundidad,nodo)
    
        downleft = [nodo.posc()[0]+2,nodo.posc()[1]-1]
        if downleft[0] <= len(nodo.entorno) - 1 and downleft[1] >=0:
            if nodo.entorno[downleft[0]][downleft[1]] == 0:
                self.movimientos.append(Nodo(nodo.mover(5,_color)),_tipo,nodo.utilidad(limit_profundidad),self.profundidad,nodo)
    
        leftdown = [nodo.posc()[0]+1,nodo.posc()[1]-2]
        if leftdown[1] >= 0 and leftdown[0] <= len(nodo.entorno) - 1:
            if nodo.entorno[leftdown[0]][leftdown[1]] == 0:
                self.movimientos.append(Nodo(nodo.mover(6,_color)),_tipo,nodo.utilidad(limit_profundidad),self.profundidad,nodo)
        
        leftup = [nodo.posc()[0]-1,nodo.posc()[1]-2]
        if leftup[1] >= 0 and leftup[0] >=0:
            if nodo.entorno[leftup[0]][leftup[1]] == 0:
                self.movimientos.append(Nodo(nodo.mover(7,_color)),_tipo,nodo.utilidad(limit_profundidad),self.profundidad,nodo)

        upleft = [nodo.posc()[0]-2,nodo.posc()[1]-1]
        if upleft[1] >= 0 and upleft[0] >=0:
            if nodo.entorno[upleft[0]][upleft[1]] == 0:
                self.movimientos.append(Nodo(nodo.mover(8,_color)),_tipo,nodo.utilidad(limit_profundidad),self.profundidad,nodo)
        
        return self.crearArbol(self.movimientos.pop(0),limit_profundidad)
