import pygame
import numpy as np
import random
import sys
from Juego import Juego
from Nodo import Nodo



class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, 0, 0, 1, 1)

    def updatecursor(self):
        (self.left, self.top) = pygame.mouse.get_pos()


class Button(pygame.sprite.Sprite):

    def __init__(self, image1, image2, x=0, y=10):
        self.imagen_normal = image1
        self.imagen_seleccion = image2
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left, self.rect.top = (x, y)
        self.x = x
        self.y = y

    def update(self, pantalla, cursor, show):
        if cursor.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccion
        else:
            self.imagen_actual = self.imagen_normal
        if show:
            self.rect.left, self.rect.top = (self.x, self.y)
            pantalla.blit(self.imagen_actual, self.rect)
        else:
            self.rect.left, self.rect.top = (-100, -100)

class Fuente:
    BLANCO = (255, 255, 255)
    VERDE = (3, 175, 80)
    ROJO = (255, 0, 0)
    AMARILLO = (231, 242, 0)

    def __init__(self, fuente, size, texto, coor):
        self.fuente = fuente
        self.size = size
        self.font = pygame.font.SysFont(fuente, size)
        self.texto = texto
        self.coor = coor
        self.rect = pygame.Rect(coor[0], coor[1], len(texto) * 10, (len(texto) / 3) * 10)

    def set_size(self, size):
        self.font = pygame.font.SysFont(self.fuente, size)

    def underline(self, bool):
        self.font.set_underline(bool)

    def render(self, antialias= 0, cursor=None):
        color = self.VERDE
        if not cursor is None:
            if cursor.colliderect(self.rect):
                color = self.AMARILLO
        return self.font.render(self.texto, antialias, color)


class Ventana:
    # Definimos algunos colores
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    VERDE = (3, 175, 80)
    ROJO = (255, 0, 0)
    AMARILLO = (231, 242, 0)
    CAFE = (172, 76, 13)
    ROSADO = (249, 128, 186)

    def __init__(self, largo=800, alto=600):
        # Inicializamos pygame
        pygame.init()
        # variables
        self.salir = False
        # Establecemos el LARGO y ALTO de la pantalla
        flags = pygame.RESIZABLE# | pygame.SCALED
        self.dimension_ventana = [largo , alto]
        self.pantalla = pygame.display.set_mode(self.dimension_ventana, flags)
        # Establecemos el título de la pantalla.
        pygame.display.set_caption("Proyecto 2 IA")
        # Lo usamos para establecer cuán rápido de refresca la pantalla.
        self.reloj = pygame.time.Clock()
        # cursor
        self.cursor = Cursor()

class Tablero(Ventana):

    def __init__(self, grid=[], pasos=[], paso_actual=0, nivel=1, largo=50, alto=50, margen=5):
        #grid
        self.grid = pasos[paso_actual] if len(pasos) > 0 else grid
        self.grid_inicial = self.grid
        self.pasos = pasos
        #nivel
        self.nivel = nivel
        #largo y alto
        self.largo = largo
        self.alto = alto
        # Establecemos el margen entre las celdas.
        self.margen = margen
        alto_m = len(self.grid)
        largo_m = len(self.grid[0])
        margen_total = ((self.margen * 10) + 5)
        ##inicializamos pygame
        super().__init__(largo_m * margen_total, alto_m * margen_total)
        self.paso_actual = paso_actual
        self.caballo = None
        self.bonus = None
        self.inicializar_imagenes()


    def inicializar_imagenes(self):
        self.caballo = pygame.image.load("img/caballo.png").convert()
        self.caballo.set_colorkey(self.NEGRO)
        self.bonus = pygame.image.load("img/bonus.png").convert()
        self.bonus.set_colorkey(self.NEGRO)

    def set_pos_ant(self):
        pos_ant = list(map(lambda x: x[0], np.where(self.grid == 2)))
        self.grid[pos_ant[0]][pos_ant[1]] = 0

    def update_pos_pasos(self, paso):
        op = self.paso_actual + paso
        if op >= len(self.pasos):
            self.paso_actual = 0
            self.mostrar = False
        elif op < 0:
            self.paso_actual = len(self.pasos) - 1
        else:
            self.paso_actual = op

    def loop_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.salir = True
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    pass
                    # if self.cursor.colliderect(self.atras):
                    #     self.estado_interfaz = 0
                    #     self.pasos = []
                    #     self.grid = self.grid_inicial
                    #     self.resultados = ["", "", ""]
                    #     self.busqueda.reset_result()

            if evento.type == pygame.KEYDOWN:
                if len(self.pasos) > 0:
                    if evento.key == pygame.K_RIGHT:
                        self.update_pos_pasos(1)
                    if evento.key == pygame.K_LEFT:
                        self.update_pos_pasos(-1)

    def dibujar_imagen(self, imagen, columna, fila):
        self.pantalla.blit(
            imagen,
            [
                (self.margen + self.largo) * columna + self.margen,
                (self.margen + self.alto) * fila + self.margen
            ]
        )

    def set_grid(self):
        if len(self.pasos) > 0:
            if self.paso_actual == 0:
                self.grid = self.pasos[0]
            else:
                self.grid = self.pasos[self.paso_actual]

    def draw_loop(self):
        # Dibujamos la retícula
        self.set_grid()
        for fila in range(len(self.grid)):
            for columna in range(len(self.grid[0])):
                color = self.BLANCO
                if self.grid[fila][columna] == 1:
                    color = self.VERDE
                if self.grid[fila][columna] == 2:
                    color = self.ROJO
                if self.grid[fila][columna] == 4:
                    color = self.VERDE
                if self.grid[fila][columna] == 5:
                    color = self.ROJO

                pygame.draw.rect(self.pantalla,
                                 color,
                                 [(self.margen + self.largo) * columna + self.margen,
                                  (self.margen + self.alto) *
                                  fila + self.margen,
                                  self.largo,
                                  self.alto])

                # pintar imagenes
                if self.grid[fila][columna] == 1 or self.grid[fila][columna] == 2:
                    self.dibujar_imagen(self.caballo, columna, fila)
                if self.grid[fila][columna] == 3:
                    self.dibujar_imagen(self.bonus, columna, fila)

    def main_loop(self):
        # -------- Bucle Principal del Programa-----------
        while not self.salir:
            self.loop_events()

            self.reloj.tick(60)

            # Establecemos el fondo de pantalla.
            self.pantalla.fill(self.NEGRO)

            self.draw_loop()

            # actualizar rectangulo de cursor
            self.cursor.updatecursor()
            # self.busqueda_no_inf.update(
            #     self.pantalla, self.cursor, self.estado_interfaz == 0)

            # Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
            pygame.display.flip()

        # Pórtate bien con el IDLE.
        pygame.quit()
        Menu().show_window()

    def show_window(self):
        self.main_loop()

class Menu(Ventana):

    def __init__(self, largo=600, alto=400):
        #largo y alto
        self.largo = largo
        self.alto = alto
        ##inicializamos pygame
        super().__init__(largo, alto)

        x = (self.dimension_ventana[0]/2)
        y = 20
        self.titulo = Fuente('Gabriola', 50, "War Horses", (x - 7 * 10, y))
        self.principiante = Fuente('Gabriola', 34, "principiante", (x - 5.5 * 10, y + 100))
        self.amateur = Fuente('Gabriola', 34, "amateur", (x - 3.5 * 10, y + 170))
        self.experto = Fuente('Gabriola', 34, "experto", (x - 3.5 * 10, y + 240))

    def iniciar_nivel(self, nivel):
        grid = np.zeros([8, 8], dtype=int)
        _range = range(0, 8)
        caballo1 = np.array(random.sample(_range, 2))
        caballo2 = np.empty([1])
        while True:
            caballo2 = np.array(random.sample(_range, 2))
            if np.array_equal(caballo1, caballo2) is False:
                break

        bono = []
        bono2 = []
        bono3 = []
        while True:
            bono = np.array(random.sample(_range, 2))
            bono2 = np.array(random.sample(_range, 2))
            bono3 = np.array(random.sample(_range, 2))

            if sum(np.absolute(bono - bono2)) > 1 and sum(np.absolute(bono2 - bono3)) > 1 and \
                    np.array_equal(bono, caballo1) is False and \
                    np.array_equal(bono, caballo2) is False and \
                    np.array_equal(bono2, caballo1) is False and \
                    np.array_equal(bono2, caballo2) is False and \
                    np.array_equal(bono3, caballo1) is False and \
                    np.array_equal(bono3, caballo2) is False:
                break
        chars = [[caballo1, 1], [caballo2, 2], [bono, 3], [bono2, 3], [bono3, 3]]
        for char in chars:
            grid[char[0][0]][char[0][1]] = char[1]
        print(grid)

        Tablero(grid=grid, nivel=nivel).show_window()

    def loop_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit(0)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.cursor.colliderect(self.principiante.rect):
                        self.iniciar_nivel(1)
                        self.salir = True
                    if self.cursor.colliderect(self.amateur.rect):
                        self.iniciar_nivel(2)
                        self.salir = True
                    if self.cursor.colliderect(self.experto.rect):
                        self.iniciar_nivel(3)
                        self.salir = True

    def main_loop(self):
        # -------- Bucle Principal del Programa-----------
        while not self.salir:
            self.loop_events()

            self.reloj.tick(60)

            # Establecemos el fondo de pantalla.
            self.pantalla.fill(self.NEGRO)

            self.pantalla.blit(
                self.titulo.render(),
                self.titulo.coor
            )

            self.pantalla.blit(
                self.principiante.render(cursor=self.cursor),
                self.principiante.coor
            )

            self.pantalla.blit(
                self.amateur.render(cursor=self.cursor),
                self.amateur.coor
            )

            self.pantalla.blit(
                self.experto.render(cursor=self.cursor),
                self.experto.coor
            )

            # actualizar rectangulo de cursor
            self.cursor.updatecursor()

            # Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
            pygame.display.flip()

        # Pórtate bien con el IDLE.
        pygame.quit()

    def show_window(self):
        self.main_loop()

# Menu().show_window()

#---------------------------------------------
grid = np.loadtxt('entorno.txt', dtype=int)
nodo = Nodo(grid,1)
jugadas=Juego().crearArbol(nodo,4,0,[nodo])
jugada=Juego().minimax(jugadas)
Tablero(grid=jugada.entorno).show_window()