import pygame
import numpy as np
import random
from Juego import Juego
from Nodo import Nodo
import time
import sys
import gc


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

    def __init__(self, fuente, size, texto, coor, color=None):
        self.fuente = fuente
        self.size = size
        self.font = pygame.font.SysFont(fuente, size)
        self.texto = texto
        self.coor = coor
        self.rect = pygame.Rect(coor[0], coor[1], len(
            texto) * 10, (len(texto) / 3) * 10)
        self.color = color if not color is None else [
            self.VERDE, self.AMARILLO]

    def set_size(self, size):
        self.font = pygame.font.SysFont(self.fuente, size)

    def underline(self, bool):
        self.font.set_underline(bool)

    def render(self, antialias=0, cursor=None):
        color = self.color[0]
        if not cursor is None:
            if cursor.colliderect(self.rect):
                color = self.color[1]
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
        flags = pygame.RESIZABLE  # | pygame.SCALED
        self.dimension_ventana = [largo, alto]
        self.pantalla = pygame.display.set_mode(self.dimension_ventana, flags)
        # Establecemos el título de la pantalla.
        pygame.display.set_caption("Proyecto 2 IA")
        # Lo usamos para establecer cuán rápido de refresca la pantalla.
        self.reloj = pygame.time.Clock()
        # cursor
        self.cursor = Cursor()


class Tablero(Ventana):
    DIFICULTAD = [2, 4, 6]

    def __init__(self, grid=[], largo=50, alto=50, margen=5):
        # grid
        self.grid = np.zeros([8, 8], dtype=int)
        self.grid_inicial = self.grid
        # nivel
        self.nivel = None
        # largo y alto
        self.ancho = largo
        self.alto = alto
        # Establecemos el margen entre las celdas.
        self.margen = margen
        alto_m = len(self.grid)
        largo_m = len(self.grid[0])
        margen_total = ((self.margen * 10) + 5)
        # inicializamos pygame
        super().__init__(largo_m * margen_total, (alto_m * margen_total)+100)
        self.caballo = None
        self.bonus = None
        self.inicializar_imagenes()
        self.turno = 1
        self.fin = False
        self.profundidad = None
        self.time_init = time.time()
        self.jugadas_1 = []
        self.jugadas_2 = []
        self.muestra = False
        self.calcular = False
        x = (self.dimension_ventana[0] / 2)
        y = 100
        self.titulo = Fuente('Gabriola', 50, "War Horses", (x - 7 * 10, y))
        self.principiante = Fuente(
            'Gabriola', 34, "principiante", (x - 5.5 * 10, y + 100))
        self.amateur = Fuente('Gabriola', 34, "amateur",
                              (x - 3.5 * 10, y + 170))
        self.experto = Fuente('Gabriola', 34, "experto",
                              (x - 3.5 * 10, y + 240))
        self.menu = True

    def inicializar_imagenes(self):
        self.caballo = pygame.image.load("img/caballo.png").convert()
        self.caballo.set_colorkey(self.NEGRO)
        self.bonus = pygame.image.load("img/bonus.png").convert()
        self.bonus.set_colorkey(self.NEGRO)

    def pos_mouse(self):
        pos = pygame.mouse.get_pos()
        return (
            (pos[1] // (self.ancho + self.margen))-2,
            (pos[0] // (self.alto + self.margen))
        )

    def loop_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.grid = np.zeros([8, 8], dtype=int)
                self.grid_inicial = self.grid
                self.turno = 1
                self.fin = False
                self.profundidad = None
                self.jugadas_1 = []
                self.jugadas_2 = []
                self.muestra = False
                self.calcular = False
                self.menu = True
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and self.turno == 2:
                    mov = list(
                        filter(lambda x: (x[self.pos_mouse()] == 1), self.jugadas_2))
                    if len(mov) > 0:
                        self.grid = mov[0]
                        self.grid_inicial = self.grid
                        self.turno = 1
                        self.time_init = time.time()
                        self.jugadas_2 = []

    def dibujar_imagen(self, imagen, columna, fila):
        self.pantalla.blit(
            imagen,
            [
                ((self.margen + self.ancho) * columna + self.margen),
                ((self.margen + self.alto) * fila + self.margen) + 100
            ]
        )

    def jugadasj(self):
        return np.count_nonzero(np.array(self.grid_inicial) == 4) + 1

    def jugadasm(self):
        return np.count_nonzero(np.array(self.grid_inicial) == 5) + 1

    def ganador(self):
        if self.jugadasm() == self.jugadasj():
            return "Empate"
        elif self.jugadasm() > self.jugadasj():
            return "Maquina"
        else:
            return "Jugador"

    def resumen_partida(self):
        x = 0
        y = 0
        return [
            Fuente('Gabriola', 25,
                   f"Jugadas maquina: {self.jugadasm()}", (x, y)),
            Fuente('Gabriola', 25,
                   f"Jugadas jugador: {self.jugadasj()}", (x + 280, y)),
            Fuente('Gabriola', 25, "Turno " +
                   ("Maquina" if self.turno == 1 else "Jugador"), (x, y + 30)),
            Fuente('Gabriola', 25, ("Maquina" if self.turno ==
                   1 else "Jugador"), (x + 5*10, y + 30), [self.AMARILLO]),
        ]

    def draw_resumen(self):
        for fuente in self.resumen_partida():
            self.pantalla.blit(
                fuente.render(),
                fuente.coor
            )

    def draw_ganador(self):
        self.pantalla.blit(
            Fuente('Gabriola', 27, f"{'Hay' if self.ganador() == 'Empate' else 'Ganador'} {self.ganador()}!!", (0, 60), [
                   self.AMARILLO]).render(),
            (0, 60)
        )

    def draw_loop(self):
        mov = list(
            filter(lambda x: (x[self.pos_mouse()] == 1), self.jugadas_2))

        if len(mov) > 0:
            self.muestra = True
            self.grid = mov[0]
        else:
            self.muestra = False
            self.grid = self.grid_inicial

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
                                 [(self.margen + self.ancho) * columna + self.margen,
                                  ((self.margen + self.alto)
                                   * fila + self.margen) + 100,
                                  self.ancho,
                                  self.alto])

                # pintar imagenes
                if self.grid[fila][columna] == 1 or self.grid[fila][columna] == 2:
                    self.dibujar_imagen(self.caballo, columna, fila)
                if self.grid[fila][columna] == 3:
                    self.dibujar_imagen(self.bonus, columna, fila)

    def calcular_mov_jug(self):
        if self.turno == 2 and self.fin is False and self.muestra is False:
            nodo = Nodo(self.grid, 2)
            self.jugadas_2 = list(
                map(lambda x: x.entorno, Juego().crearArbol(1, [nodo])))
            if len(self.jugadas_2) == 1:
                self.turno = 1

    def turno_maq(self):
        # turnos
        if self.turno == 1 and self.fin is False and self.muestra is False:
            _time = (time.time() - self.time_init)
            delay = 0.3 if len(self.jugadas_2) == 1 else 1.5
            if _time <= delay:
                return
            nodo = Nodo(self.grid, 1)
            self.jugadas_1 = Juego().crearArbol(self.profundidad, [nodo])
            if len(self.jugadas_1) > 1:
                jugadas = list(np.copy(self.jugadas_1))
                self.grid = Juego().recorrerMinimax(jugadas, self.profundidad).entorno
                self.grid_inicial = self.grid
            self.turno = 2
            self.time_init = time.time()

        # print(f"jugadas 1: {len(self.jugadas_1)}  and jugadas 2: {len(self.jugadas_2)}")
        if len(self.jugadas_1) == 1 and len(self.jugadas_2) == 1:
            # print(self.grid)
            self.fin = True

    def main_loop(self):
        # -------- Bucle Principal del Programa-----------
        while not self.salir:
            if self.menu:
                self.menu_loop()
            else:
                self.loop_events()
                if self.menu:
                    continue
                self.reloj.tick(60)

                # Establecemos el fondo de pantalla.
                self.pantalla.fill(self.NEGRO)

                self.turno_maq()
                self.draw_loop()

                self.calcular_mov_jug()

                self.draw_resumen()

                if self.fin:
                    self.draw_ganador()

                # actualizar rectangulo de cursor
                self.cursor.updatecursor()

                # Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
                pygame.display.flip()

        # Pórtate bien con el IDLE.
        pygame.quit()

    def show_window(self):
        self.main_loop()

    def iniciar_nivel(self):
        random.seed(a=time.time(), version=2)
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
            if sum(np.absolute(bono - bono2)) > 2 and sum(np.absolute(bono2 - bono3)) > 2 and \
                sum(np.absolute(bono - bono3)) > 2 and np.array_equal(bono, caballo1) is False and \
                    np.array_equal(bono, caballo2) is False and \
                    np.array_equal(bono2, caballo1) is False and \
                    np.array_equal(bono2, caballo2) is False and \
                    np.array_equal(bono3, caballo1) is False and \
                    np.array_equal(bono3, caballo2) is False:
                break
        chars = [[caballo1, 1], [caballo2, 2],
                 [bono, 3], [bono2, 3], [bono3, 3]]
        for char in chars:
            self.grid[char[0][0]][char[0][1]] = char[1]
        #grid = np.loadtxt('entorno.txt', dtype=int)
        self.profundidad = self.DIFICULTAD[self.nivel]
        self.time_init = time.time()

    def loop_events_menu(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if self.menu:
                    sys.exit(0)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.cursor.colliderect(self.principiante.rect):
                        self.nivel = 0
                        self.iniciar_nivel()
                        self.menu=False
                    if self.cursor.colliderect(self.amateur.rect):
                        self.nivel = 1
                        self.iniciar_nivel()
                        self.menu = False
                    if self.cursor.colliderect(self.experto.rect):
                        self.nivel = 2
                        self.iniciar_nivel()
                        self.menu = False

    def menu_loop(self):
        self.loop_events_menu()

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


Tablero().show_window()
