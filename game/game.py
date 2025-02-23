import pygame
import sys
from .config import *
from .Platform import Platform
from .player import Player
from .wall import Wall
import random
from .coin import Coin
import os


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode(
            (WHIDTH, HEIGHT))  # creamos la pantalla y se lo asignamos a un atributo
        # le asignamos un nombre a la ventana
        pygame.display.set_caption(TITLE)
        self.running = True  # Este atributo es para saber si esta ejecutandoce la app

        self.clock = pygame.time.Clock()
        # es para obtener la ruta absoluta de un archivo
        self.dir = os.path.dirname(__file__)
        self.dir_sounds = os.path.join(
            self.dir, "sounds")  # ruta de carpeta de sonido
        self.font = pygame.font.match_font(font)
        self.dir_images = os.path.join(self.dir, "sprites")

    def start(self):
       # self.menu()  # NO FUNCIONA
        self.new()  # ejecuta el metodo new

    def new(self):
        self.score = 0
        self.level = 0
        self.playing = True
        self.generate_elements()
        self.run()  # ejecuta el metodo run
        self.blackgraund = pygame.image.load(os.path.join(
            self.dir_images, "desierto.png"))  # esto seria para cargar la
        # la imagen de atras pero no me funciono

    def run(self):
        while self.running:
            self.clock.tick(fps)
            self.events()

            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():  # creamos el evento para cerrar la ventana
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.player.jump()
        if key[pygame.K_r] and not self.playing:
            self.new()

    def draw(self, pos=0):
        # colocamos la imagen de fondo

        fondo = [(pygame.image.load(
            os.path.join(self.dir_images, "desierto.png"))), (pygame.image.load(
                os.path.join(self.dir_images, "deS_tarde.jpg")))]
        self.surface.blit((fondo[pos]), (0, 0))

        self.sprite.draw(self.surface)
        self.draw_text()

        pygame.display.flip()  # para refrescar la pantalla escomo el metodo update

    def update(self):

        if self.playing:

            wall = self.player.collide_with(self.walls)
            if wall:
                # si el jugador toca el cuadrado de top wall
                if self.player.collide_bottom(wall):
                    self.player.skid(wall)
                else:
                    self.stop()

            coin = self.player.collide_with(self.coins)
            if coin:
                self.score += 1
                coin.kill()

                sound = pygame.mixer.Sound(
                    os.path.join(self.dir_sounds, "coin.wav"))
                sound.play()
            self.sprite.update()  # todos los sprit de la lista ejecutaran su metodo Update
            # ejecutamos el modulo de validacion y enviamos la plataforma
            self.player.validate_platform(self.platform)
            # elimina las walls que ya pasaron
            self.update_elements(self.walls)
            self.update_elements(self.coins)  # elimina las monedas que tomo
            self.gerenate_walls()

    def stop(self):
        sound = pygame.mixer.Sound(
            os.path.join(self.dir_sounds, "lose.wav"))
        sound.play()
        self.player.stop()
        self.stop_elements(self.walls)
        self.playing = False

    def stop_elements(self, elements):
        for element in elements:
            element.stop()

    def generate_elements(self):
        self.platform = Platform()  # generamos la plataforma
        self.player = Player(100, self.platform.rect.top -
                             200, self.dir_images)  # Generamos player

        # Permite agrupar los sprite, esto es una lista
        self.sprite = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()  # grupo de walls
        self.coins = pygame.sprite.Group()  # grupo de coins
        self.sprite.add(self.platform)  # lo agregamos a la lista
        self.sprite.add(self.player)

        self.gerenate_walls()  # generamos walls

    def generate_coins(self):

        last_position = WHIDTH+100  # intervalo de colocacion de monedas
        for c in range(0, max_coins):
            pos_x = random.randrange(last_position+150, last_position+300)
            # genera las monedas y la coloca a 100 pix de altura
            coin = Coin(pos_x, 100, self.dir_images)
            last_position = coin.rect.right
            self.sprite.add(coin)  # almacenamos coin en lista de sprits
            self.coins.add(coin)  # almacenamos coin en la lista de coins

    def gerenate_walls(self):

        last_position = WHIDTH+100

        if not len(self.walls) > 0:  # si no existen obstaculos
            for w in range(0, max_walls):
                left = random.randrange(last_position + 200, last_position+400)
                wall = Wall(left, self.platform.rect.top, self.dir_images)
                last_position = wall.rect.right
                self.sprite.add(wall)
                self.walls.add(wall)
            self.level += 1  # subo de nivel cuando se genera un nivel nuevo de obstaculo

            # self.draw(self.level)  # revisarno funciona

            self.generate_coins()  # genera monedas para el nuevo nivel

    def update_elements(self, elements):
        for element in elements:
            if not element.rect.right > 0:
                element.kill()

    def score_format(self):
        return "store : {}".format(self.score)

    def level_format(self):
        return "Level : {}".format(self.level)

    def draw_text(self):
        self.displey_text(self.score_format(), 30, black, WHIDTH//2, tex_pos_y)
        self.displey_text(self.level_format(), 30, black, 60, tex_pos_y)
        if not self.playing:
            self.displey_text("Game Over", 30, black, WHIDTH//2, HEIGHT//2)
            self.displey_text(
                "Presiona R para comensar de nuevo", 30, black, WHIDTH//2, 100)

    # texto, tipo de letra,color, pinta texto en pantalla

    def displey_text(self, text, size, color, pos_x, pos_y):
        font = pygame.font.Font(self.font, size)
        text = font.render(text, True, color)
        rect = text.get_rect()
        rect.midtop = (pos_x, pos_y)  # posiciono el tecto
        self.surface.blit(text, rect)

    def menu(self):
        self.surface.fill(green_light)
        self.displey_text("Preciona una tecla para comenzar",
                          60, black, WHIDTH//2, 10)
        pygame.display.flip()  # actualiza pantalla
        self.wait()

    def wait(self):
        wait = True

        while wait:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event == pygame.KEYUP:
                    wait = True
