import pygame
import numpy as np
from busqueda import Busqueda
import random


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


class Interfaz:
    # Definimos algunos colores
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    VERDE = (3, 175, 80)
    ROJO = (255, 0, 0)
    AMARILLO = (231, 242, 0)
    CAFE = (172, 76, 13)
    ROSADO = (249, 128, 186)

    def __init__(self, grid=[], pasos=[], paso_actual=0, largo=50, alto=50, margen=5):
        # Inicializamos pygame
        pygame.init()
        # variables
        self.salir = False
        self.grid = pasos[paso_actual] if len(pasos) > 0 else grid
        self.grid_inicial = self.grid
        self.pasos = pasos
        self.paso_actual = paso_actual
        # Establecemos el LARGO y ALTO de cada celda de la retícula.
        self.largo = largo
        self.alto = alto
        # Establecemos el margen entre las celdas.
        self.margen = margen
        alto_m = len(self.grid)
        largo_m = len(self.grid[0])
        margen_total = ((self.margen * 10) + 5)
        # Establecemos el LARGO y ALTO de la pantalla
        flags = pygame.RESIZABLE# | pygame.SCALED
        self.dimension_ventana = [largo_m * margen_total, alto_m * margen_total]
        self.pantalla = pygame.display.set_mode(self.dimension_ventana, flags)
        # Establecemos el título de la pantalla.
        pygame.display.set_caption("Proyecto 2 IA")
        # Lo usamos para establecer cuán rápido de refresca la pantalla.
        self.reloj = pygame.time.Clock()
        # Se usa para saber que botones se muestran
        self.estado_interfaz = 0
        # Texto informes
        self.fuente = pygame.font.SysFont("Gabriola", 27)
        # Inicializamos imagenes
        self.caballo = None
        self.bonus = None
        self.inicializar_imagenes()
        # cursor
        self.cursor = Cursor()
        # Botones
        self.inicializar_botones()
        # utils
        # self.busqueda = Busqueda(self.grid_inicial)
        self.mostrar = False

    def inicializar_imagenes(self):
        self.caballo = pygame.image.load("img/caballo.png").convert()
        self.caballo.set_colorkey(self.NEGRO)
        self.bonus = pygame.image.load("img/bonus.png").convert()
        self.bonus.set_colorkey(self.NEGRO)

    def inicializar_botones(self):
        pass
        # Botones
        # self.atras = Button(self.img_atras, self.img_atras_2,
        #                     self.dimension_ventana[0] - 200, (self.dimension_ventana[1]/2) - 50)
        # pos_y_img = (self.margen * 10) * ((len(self.grid) / 2) - 1)
        # self.busqueda_no_inf = Button(
        #     self.img_busq_no_inf, self.img_busq_no_inf_2, 0, pos_y_img)
        # self.busqueda_inf = Button(
        #     self.img_busq_inf, self.img_busq_inf_2, 0, pos_y_img + 80)
        # # --------------------------------------------
        # self.avara = Button(self.img_avara, self.img_avara_2, 0, pos_y_img)
        # self.a_estrella = Button(
        #     self.img_a_est, self.img_a_est_2, 0, pos_y_img + 80)
        # # --------------------------------------------
        # pos_y_img = (self.margen * 10) * (len(self.grid) / 3)
        # self.amplitud = Button(
        #     self.img_amplitud, self.img_amplitud_2, 0, pos_y_img)
        # self.costo = Button(
        #     self.img_costo_u, self.img_costo_u_2, 0, pos_y_img + 80)
        # self.profundidad = Button(
        #     self.img_profundidad, self.img_profundidad_2, 0, pos_y_img + 160)

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

    def post_search(self, info, tiempo):
        self.pasos = info['pasos']
        self.busqueda.reset_result()
        self.pasos.reverse()
        self.mostrar = True

        self.grid = self.pasos[0]
        self.resultados[0] = f"{round(tiempo, 3)}Seg"
        self.resultados[1] = info['profundidad']
        self.resultados[2] = info['cant_nodos_expandidos']

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
                    color = self.ROJO
                if self.grid[fila][columna] == 2:
                    color = self.VERDE

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

            if self.mostrar:
                self.update_pos_pasos(1)
                self.reloj.tick(4)
            else:
                # Limitamos a 60 fotogramas por segundo.
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

    def show_window(self):
        self.main_loop()


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

    if sum(np.absolute(bono - bono2)) > 1 and sum(np.absolute(bono2 - bono3)) > 1:
        break
chars = [[caballo1, 1], [caballo2,2], [bono,3], [bono2,3], [bono3,3]]
for char in chars:
    grid[char[0][0]][char[0][1]] = char[1]
print(grid)
Interfaz(grid=grid).show_window()
