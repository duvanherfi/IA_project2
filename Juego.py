from Nodo import Nodo,np
import sys
class Juego:
  
  def minimax(self,arbol):

    profundidadNodos = [nodo.profundidadAcumulada() for nodo in arbol]
    indexMaxProfundidadNodo = profundidadNodos.index(max(profundidadNodos))
    nodo_expandido = arbol.pop(indexMaxProfundidadNodo)
    if nodo_expandido.padre is None:
        return nodo_expandido
    if nodo_expandido.padre.tipo == 1:
        if nodo_expandido.utilidad > nodo_expandido.padre.utilidad:
            nodo_expandido.padre.utilidad = nodo_expandido.utilidad
            if nodo_expandido.profundidadAcumulada() == 1:
                nodo_expandido.padre.entorno = nodo_expandido.entorno
    else:
        if nodo_expandido.utilidad < nodo_expandido.padre.utilidad:
            nodo_expandido.padre.utilidad = nodo_expandido.utilidad
            if nodo_expandido.profundidadAcumulada() == 1:
                nodo_expandido.padre.entorno = nodo_expandido.entorno
    return self.minimax(arbol)

  def crearArbol(self,nodo,limit_profundidad,index,movimientos):
    _tipo = 0
    _color = 0
    #color = 5 -> verde, color=6->rojo
    #max = verde, min=rojo
    if nodo.tipo ==  1:
        _tipo = -1
        _color = 5
    else:
        _tipo = 1
        _color = 4

    if (nodo.profundidadAcumulada() >= limit_profundidad):
        return movimientos
    else:
        upright = [nodo.posc()[0]-2,nodo.posc()[1]+1]
        if upright[0] >= 0 and upright[1] <= len(nodo.entorno[0]) - 1:
            _pos = nodo.entorno[upright[0]][upright[1]]
            if _pos == 0 or _pos ==3:
                hijo = Nodo(nodo.mover(1,_color),_tipo,profundidad=1,padre=nodo)
                if _pos == 3:
                    hijo.aplicarBono(upright,_color)
                hijo.setUtilidad(limit_profundidad)
                movimientos.append(hijo)

        rightup = [nodo.posc()[0]-1,nodo.posc()[1]+2]
        if rightup[1] <= len(nodo.entorno[0]) - 1 and rightup[0] >=0:
            _pos = nodo.entorno[rightup[0]][rightup[1]]
            if  _pos == 0 or _pos==3:
                hijo = Nodo(nodo.mover(2,_color),_tipo,profundidad=1,padre=nodo)
                if _pos == 3:
                    hijo.aplicarBono(rightup,_color)
                hijo.setUtilidad(limit_profundidad)
                movimientos.append(hijo)
         
        rightdown = [nodo.posc()[0]+1,nodo.posc()[1]+2]
        if rightdown[1] <= len(nodo.entorno[0])-1 and rightdown[0] <= len(nodo.entorno) - 1:
            _pos = nodo.entorno[rightdown[0]][rightdown[1]]
            if _pos == 0 or _pos == 3:
                hijo = Nodo(nodo.mover(3,_color),_tipo,profundidad=1,padre=nodo)
                if _pos == 3:
                    hijo.aplicarBono(rightdown,_color)
                hijo.setUtilidad(limit_profundidad)
                movimientos.append(hijo)

        downright = [nodo.posc()[0]+2,nodo.posc()[1]+1]
        if downright[0] <= len(nodo.entorno) - 1 and downright[1] <= len(nodo.entorno[0])-1:
            _pos = nodo.entorno[downright[0]][downright[1]]
            if _pos == 0 or _pos == 3:
                hijo = Nodo(nodo.mover(4,_color),_tipo,profundidad=1,padre=nodo)
                if _pos == 3:
                    hijo.aplicarBono(downright,_color)
                hijo.setUtilidad(limit_profundidad)
                movimientos.append(hijo)

        downleft = [nodo.posc()[0]+2,nodo.posc()[1]-1]
        if downleft[0] <= len(nodo.entorno) - 1 and downleft[1] >=0:
            _pos = nodo.entorno[downleft[0]][downleft[1]]
            if _pos == 0 or _pos == 3:
                hijo = Nodo(nodo.mover(5,_color),_tipo,profundidad=1,padre=nodo)
                if _pos == 3:
                    hijo.aplicarBono(downleft,_color)
                hijo.setUtilidad(limit_profundidad)
                movimientos.append(hijo)

        leftdown = [nodo.posc()[0]+1,nodo.posc()[1]-2]
        if leftdown[1] >= 0 and leftdown[0] <= len(nodo.entorno) - 1:
            _pos = nodo.entorno[leftdown[0]][leftdown[1]]
            if _pos == 0 or _pos == 3:
                hijo = Nodo(nodo.mover(6,_color),_tipo,profundidad=1,padre=nodo)
                if _pos == 3:
                    hijo.aplicarBono(leftdown,_color)
                hijo.setUtilidad(limit_profundidad)
                movimientos.append(hijo)

        leftup = [nodo.posc()[0]-1,nodo.posc()[1]-2]
        if leftup[1] >= 0 and leftup[0] >=0:
            _pos = nodo.entorno[leftup[0]][leftup[1]]
            if _pos == 0 or _pos==3:
                hijo = Nodo(nodo.mover(7,_color),_tipo,profundidad=1,padre=nodo)
                if _pos == 3:
                    hijo.aplicarBono(leftup,_color)
                hijo.setUtilidad(limit_profundidad)
                movimientos.append(hijo)

        upleft = [nodo.posc()[0]-2,nodo.posc()[1]-1]
        if upleft[1] >= 0 and upleft[0] >=0:
            _pos = nodo.entorno[upleft[0]][upleft[1]]
            if _pos == 0 or _pos == 3:
                hijo = Nodo(nodo.mover(8,_color),_tipo,profundidad=1,padre=nodo)
                if _pos == 3:
                    hijo.aplicarBono(upleft,_color)
                hijo.setUtilidad(limit_profundidad)
                movimientos.append(hijo)
        if index + 1 >= len(movimientos):
            return movimientos
                
        return self.crearArbol(movimientos[index+1],limit_profundidad,index+1,movimientos)
